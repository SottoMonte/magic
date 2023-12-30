import WORKER
import GRAMMAR
from STRING import SPLIT
import asyncio

class MODEL():
    def ASSIGNMENT():
        exit(1)
    def CALL():
        exit(1)
    def DECLARATION():
        exit(1)

class PYTHON(MODEL):
    def ASSIGNMENT(AST):
        print(AST)
        return f"{AST[0]} = {AST[1]}\n"
    def CALL(AST):
        print(AST)
        return f"{AST[0]}{AST[1]}\n"
    def DECLARATION(AST):
        return f"{AST[0][1]} := {AST[0][0]}({AST[1][0]})\n"


def PYTHON_ASSIGNMENT(AST) -> str:
    print(AST)
    return f"{AST[0]} = {AST[1]}\n"

def PYTHON_CALL(AST) -> str:
    print(AST)
    return f"{AST[0]}{AST[1]}\n"

def PYTHON_DECLARATION(AST) -> str:
    return f"{AST[0][1]} := {AST[0][0]}({AST[1][0]})\n"

async def CODE(WORKER:WORKER.WORKER):
    '''
    ||| Ascolta finche non riceve AST
    '''
    while True:  
        AST = await WORKER.HEAR()
        if AST != None:break
    #print("ricevuto")
    '''
    ||| Apre un file in scrittura
    '''
    open('code.py', 'w').close()
    f = open("code.py", "a+")
    file = ""
    print(f"Code:{AST}")
    '''
    ||| Controlla il primo livello AST e per ogni istruzione la codifica
    '''
    for INSTRUCTION in AST[1]:
        match INSTRUCTION[0]:
            case GRAMMAR.INSTRUCTION_CALL.__name__:
                file += PYTHON_CALL(INSTRUCTION[1])
            case GRAMMAR.INSTRUCTION_DECLARATION.__name__:
                file += PYTHON_DECLARATION(INSTRUCTION[1])
            case GRAMMAR.INSTRUCTION_ASSIGNMENT.__name__:
                file += PYTHON_ASSIGNMENT(INSTRUCTION[1])

    f.write(file)
    f.close()
    pass