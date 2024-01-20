import sys
sys.path.append('src/core/')
import worker
import grammar
#from STRING import SPLIT
import asyncio


def NAME(DB,TARGET,CHECK):
    type_value = TARGET[1][0]
    #value = INSTRUCTION[1][1][1]
    name = TARGET[0][1]
    type = TARGET[0][0]
    if name not in DB:
        print("true")
        return 
    else:
        print(f"VARIABILE {name} NON DECHIARATA")
        return None

def TYPE(DB,NAME,VALUE):
    TARGET = DB[NAME]
    CHECK = VALUE[0]

    if(TARGET != VALUE):return False
    else:return True 

async def VALIDATOR(WORKER:worker.WORKER):
    '''
    ||| Spazio nomi
    '''
    NameSpace = dict()
    '''
    ||| Ascolta finche non riceve AST
    '''
    while True:
        AST = await WORKER.HEAR()
        await WORKER.ECHO(AST)
        if AST == 0:break
    '''
    ||| Valida le istruzioni sicurezza tipi, gestione della memoria, gestione variabili
    '''
    '''for INSTRUCTION in AST[1]:
        print(NameSpace)
        match INSTRUCTION[0]:
            case GRAMMAR.INSTRUCTION_CALL.__name__:
                if INSTRUCTION[1][0] in NameSpace:
                    pass
                else:
                    print("CALL:La chiave k non esiste nel dizionario d.")
                    
            case GRAMMAR.INSTRUCTION_DECLARATION.__name__:
                #(TYPE:ID,TYPE:VALUE|ID)
                con = INSTRUCTION[1][1]
                type_value = INSTRUCTION[1][1][0]
                value = INSTRUCTION[1][1][1]
                name = INSTRUCTION[1][0][1]
                type = INSTRUCTION[1][0][0]
                
                if name not in NameSpace:
                    if type_value == GRAMMAR.IDENTIFIER.__name__:
                        if value in NameSpace:
                            if type == NameSpace[value][0]:
                                NameSpace[name] = NameSpace[name2]
                                INSTRUCTION[1][1] = NameSpace[name][1]
                            else:print(f"Errore tipo {type} != {NameSpace[name2][0]}")
                        else:print(f"VARIABILE {value} NON DECHIARATA")

                else:print(f"VARIABILE {name} NON DECHIARATA")
                

                if name not in NameSpace:
                    print("-->",name,con[1][0])
                    name2 = con[1][0]
                    if type_value == GRAMMAR.IDENTIFIER.__name__:
                        print("#####")
                        if con[1][0] in NameSpace:
                            if type == NameSpace[name2][0]:
                                print(type,NameSpace[name2][0])
                            else:
                                print(f"Errore tipo {type} != {NameSpace[name2][0]}")
                            NameSpace[name] = NameSpace[name2]
                            INSTRUCTION[1][1] = NameSpace[name][1]
                        else:
                            print("&&&",con)
                            NameSpace[name] = con 
                    else:
                        print("$$",con)
                        NameSpace[name] = con
                else:
                    print(f"VARIABILE {name} NON DECHIARATA")


                
            case GRAMMAR.INSTRUCTION_ASSIGNMENT.__name__:
                

                name = INSTRUCTION[1][0]
                con = INSTRUCTION[1][1]
                print(name,con)
                if name in NameSpace:
                    if GRAMMAR.IDENTIFIER(con)[0]:
                        if con in NameSpace:
                            NameSpace[name] = NameSpace[con]
                    else: NameSpace[name] = con
                else:
                    print(f"VARIABILE {name} NON DECHIARATA")
                    
                print(INSTRUCTION[1][0])'''
    '''
    ||| Invia il flusso validato a generatore
    '''
    #await WORKER.SPEAK('CODE',AST)