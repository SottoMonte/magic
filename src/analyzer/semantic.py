import sys
sys.path.append('src/core/')
import worker as WORKER
import data as DATA
import grammar
import syntax
#from STRING import SPLIT
import asyncio

# elencami 20 tipi di errore del compilatore come nome variabile gia utillizato per il namespace
'''
# http://www.di.uniba.it/~lops/linguaggi/TabellaSimboli.pdf
# https://learn.microsoft.com/it-it/cpp/error-messages/compiler-errors-1/compiler-error-c2065?view=msvc-170
# In breve, l'analisi semantica si concentra sulla correttezza del significato del codice, garantendo che sia coerente con la definizione del linguaggio.
- Validazione semantica
- Errori semantici
- Verifica del tipo
- Controllo del flusso
- Semantica statica e dinamica
'''

async def CALCULATE_VALUE(worker,value,symbolTable):
    #print(type(value),value)
    if isinstance(value,tuple):
        if isinstance(value[0],tuple):
            a = CALCULATE_VALUE(value[0])
        elif value[0].isalpha():
            _,a = await VALUE(worker,value[0],symbolTable)
        else:
            a = value[0]

        if isinstance(value[2],tuple):
            b = CALCULATE_VALUE(value[2])
        elif value[2].isalpha():
            _,b = await VALUE(worker,value[2],symbolTable)
        else:
            b = value[2]
        #print("###->",a,value.data,b)

        match value[1]:
            case '+': return int(a) + int(b)
            case '-': return int(a) - int(b)
            case '*': return int(a) * int(b)
            case '/': return int(a) / int(b)
    else:
        return value


async def VALUE(worker,value,symbolTable):
    
    async def block_error (worker,**constants):
        worker.app.logger.critical(f"SemanticError{VALUE.__name__[0] + VALUE.__name__[1:].lower()}: '{value}': value was not passed")
        return [None],value
    async def block_number (worker,**constants): return ['INTEGER','NATURAL'],value
    async def block_string (worker,**constants): return ['STRING'],value
    async def block_id (worker,**constants): 
        if value in symbolTable.value:
            a = await WORKER.GET(worker,f'SymbolTable.{value}')
            return [a.value['type']],a.value['value']
        else:
            worker.app.logger.critical(f"SemanticError{VALUE.__name__[0] + VALUE.__name__[1:].lower()}: '{value}': undeclared identifier")
            return [None],value
    async def block_arithmetic (worker,**constants):
        #print(value)
        expression = tuple([str(i) for i in value[1:-1].split(',')])
        #print("asd",expression)
        return ['INTEGER','NATURAL'], await CALCULATE_VALUE(worker,expression,symbolTable)


    output = await WORKER.MATCH(worker,value,
        block_error,
        (grammar.AST,block_arithmetic),
        (grammar.IDENTIFIER,block_id),
        (grammar.NUMBER,block_number),
        (grammar.STRING,block_string),
        )

    print("::::::::::::::::::::>",output)

    return output

async def CALLED(worker,SymbolTable,identifier,typee,value):
    #worker.app.logger.critical(f"SemanticError{CALLED.__name__[0] + CALLED.__name__[1:].lower()}: '{identifier}': some parameters are missing")
    #worker.app.logger.critical(f"SemanticError{CALLED.__name__[0] + CALLED.__name__[1:].lower()}: '{identifier}': some parameters are unnecessary")
    if False:
        pass
    else:
       worker.app.logger.critical(f"SemanticError{CALLED.__name__[0] + CALLED.__name__[1:].lower()}: '{identifier}': identifier is not a function")

async def ALLOCATION(worker,SymbolTable,identifier,typee,value):
    tipi,valor = await VALUE(worker,value,SymbolTable)

    # Type Checking: Verifica la correttezza dei tipi delle variabili e delle espressioni. Un semantic compiler segnala errori se si tenta di assegnare un valore di tipo errato a una variabile o di utilizzare un’operazione non consentita tra tipi incompatibili.
    Type_Checking = False
    for tipo in  tipi:
        if typee == tipo: 
            Type_Checking = True
            break
    if Type_Checking == False: worker.app.logger.critical(f"SemanticError{ALLOCATION.__name__[0] + ALLOCATION.__name__[1:].lower()}: '{identifier}': incorrect type value")
    
    # Gestione delle Variabili: Un semantic compiler tiene traccia delle variabili, delle loro dichiarazioni e dei loro ambiti. Questo è essenziale per risolvere riferimenti e garantire che le variabili siano utilizzate correttamente.
    if identifier not in SymbolTable.value:
        row = {'identifier':identifier,'identity':'','address':'','dimension':'','type':typee,'value':valor,'lineDeclared':'','lineReferenced':''}
        a,z = await asyncio.gather(WORKER.SET(worker,'SymbolTable',{identifier:identifier}),WORKER.NEW(worker,DATA.VARIABLE(worker,'hash',f'SymbolTable.{identifier}',row)))
        #await WORKER.SET(worker,'SymbolTable',{identifier:identifier})
        #await WORKER.NEW(worker,DATA.VARIABLE(worker,'string','SymbolTable.ttt',"CIAO"))
        #a = await WORKER.GET(worker,f'SymbolTable.{identifier}')
        #print("==>",a)
    else:
        worker.app.logger.critical(f"SemanticError{ALLOCATION.__name__[0] + ALLOCATION.__name__[1:].lower()}: '{identifier}': redefinition identifier")
    

async def INSPECTOR(worker,**constants):
    ast = constants['data']
    SymbolTable = await WORKER.GET(worker,'SymbolTable')
    #print(SymbolTable)
    blocks = DATA.SPLIT(worker,DATA.VARIABLE(worker,'string','ast',ast[1:-1]),',','(',')')
    destra = "".join(blocks[2])
    mid = "".join(blocks[1])
    sinstra = "".join(blocks[0])
    #print("".join(blocks[1]),blocks)
    match mid:
        case ':=':
            typee,identifier = sinstra[1:-1].split(':')
            value = ast[1:-1].split(':=')[1][1:]
            await ALLOCATION(worker,SymbolTable,identifier,typee,value)

async def VALIDATOR(worker:WORKER.WORKER):
    '''
    ||| Variabili Globali
    '''
    await WORKER.REM(worker,'SymbolTable')
    await WORKER.NEW(worker,DATA.VARIABLE(worker,'dict','SymbolTable',{'init':100}))
    '''
    ||| Valida le istruzioni sicurezza tipi, gestione della memoria, gestione variabili
    '''
    await WORKER.EVENT(worker,'ast',INSPECTOR)
    '''
    ||| Ascolta flusso AST
    '''
    await WORKER.HEAR(worker,'ast')