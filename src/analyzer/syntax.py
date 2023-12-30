import WORKER
import GRAMMAR
from STRING import SPLIT
from BOOLEAN import OR
import asyncio

'''
# Input(TOKEN) | Output(AST)
'''
async def PARSER(WORKER:WORKER.WORKER):
    '''
    ||| Lista di tokens.
    '''
    TOKENS = list()
    '''
    ||| Ascolta tutto il flusso di tokens e lo salva in TOKENS.
    '''
    while True:  
        TOKEN = await WORKER.HEAR()
        if TOKEN == None:break
        TOKENS.append(TOKEN)
        #print("----------------------------------------=>",TOKEN)
    '''
    ||| Crea e invia un flusso di istruzioni a {SEMANTIC}.
    '''
    def UNION(TARGET):
        OUT = ""
        for ITEM in TARGET:
            OUT += ITEM
        return OUT
    '''
    ||| Generatore albero di sintassi.
    '''
    def AST(TARGET):
        TREE = []
        if type(TARGET) == type(tuple):
            print("EXITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
            return TARGET
        else:
            A = UNION(TARGET)
            CHECK,SUBJECT,DATA = OR([A],[GRAMMAR.SET,GRAMMAR.PAIR,GRAMMAR.TUPLE,GRAMMAR.STRING,GRAMMAR.NUMBER,GRAMMAR.INSTRUCTION_DECLARATION,GRAMMAR.INSTRUCTION_CALL,GRAMMAR.INSTRUCTION_ASSIGNMENT])
            print(SUBJECT)
            if CHECK == True:
                match SUBJECT[0]:
                    case GRAMMAR.INSTRUCTION_ASSIGNMENT.__name__:
                        print(f"[{GRAMMAR.INSTRUCTION_ASSIGNMENT.__name__}]")
                        return (GRAMMAR.INSTRUCTION_ASSIGNMENT.__name__,DATA[0])
                    case GRAMMAR.INSTRUCTION_CALL.__name__:
                        print(f"[{GRAMMAR.INSTRUCTION_CALL.__name__}]")
                        return (GRAMMAR.INSTRUCTION_CALL.__name__,DATA[0])
                    case GRAMMAR.INSTRUCTION_DECLARATION.__name__:
                        print(f"[{GRAMMAR.INSTRUCTION_DECLARATION.__name__}]")
                        return (GRAMMAR.INSTRUCTION_DECLARATION.__name__,DATA[0])
                    case GRAMMAR.STRING.__name__:
                        print(f"[{GRAMMAR.STRING.__name__}]")
                        return (GRAMMAR.STRING.__name__,DATA[0])
                    case GRAMMAR.NUMBER.__name__:
                        print(f"[{GRAMMAR.NUMBER.__name__}]")
                        print(CHECK,SUBJECT[0],DATA[0])
                        return (GRAMMAR.NUMBER.__name__,DATA[0])
                    case GRAMMAR.PAIR.__name__:
                        print(f"[{GRAMMAR.PAIR.__name__}]")
                        return (GRAMMAR.PAIR.__name__,DATA[0])
                    case GRAMMAR.SET.__name__:
                        print(f"[{GRAMMAR.SET.__name__}]")
                        for X in DATA[0]:
                            TREE.append(AST(X))
                        return (GRAMMAR.SET.__name__,TREE)
                    case GRAMMAR.PAIR.__name__:
                        print(f"[{GRAMMAR.PAIR.__name__}]")
                        for X in DATA[0]:
                            TREE.append(AST(X))
                        return (GRAMMAR.PAIR.__name__,TREE)
                    case GRAMMAR.TUPLE.__name__:
                        print(f"[{GRAMMAR.TUPLE.__name__}]")
                        for X in DATA[0]:
                            TREE.append(AST(X))
                        return (GRAMMAR.TUPLE.__name__,TREE)
            else:
                # TROVA rig col di un errore
                stringa = open('sorgente.sl', 'r').read()
                sottostringa = A
                posizione = stringa.find(sottostringa)
                riga = stringa.count("\n", 0, posizione) + 1
                colonna = posizione - stringa.rfind("\n", 0, posizione)
                print(f"SyntaxError: invalid syntax [{A}] at Row {riga}-Col {colonna}")
                exit(1)
    FFF = AST(TOKENS)
    #print(FFF)
    await WORKER.SPEAK('VALIDATOR',FFF)