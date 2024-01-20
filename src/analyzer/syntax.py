import worker
import grammar
#from STRING import SPLIT
#from BOOLEAN import OR
import asyncio

'''
# Input(TOKEN) | Output(AST)
'''
async def PARSER(WORKER:worker.WORKER):
    '''
    ||| Lista di tokens.
    '''
    TOKENS = list()

    async def INSTU(self,end):
        if self[1] != '\n' and self[1] != ' ' and self[1] != "\n\n":
            INSTU.TOKENS.append(self)
        
        #for instruction in [grammar.INSTRUCTION_CALL,grammar.TUPLE,grammar.INSTRUCTION_ASSIGNMENT,grammar.INSTRUCTION_ALLOCATION,grammar.INSTRUCTION_DEALLOCATE]:
        for instruction in [grammar.INSTRUCTION_CALL,grammar.INSTRUCTION_ALLOCATION]:
            #print(len(INSTU.TOKENS),instruction.requirement())
            #if len(INSTU.TOKENS) == len(instruction.requirement()):
            if len(INSTU.TOKENS) != 0:
                dd = []
                for i in range(0,len(INSTU.TOKENS)):
                    dd.append(INSTU.TOKENS[i][1])
                
                check = instruction(WORKER,dd)
                print(dd)
                if check[0]:
                    print(check)
                    #await WORKER.ECHO(check)
                    await WORKER.SPEAK('VALIDATOR',check)
                    INSTU.TOKENS.clear()
                else:
                    print(check)
                    pass

    INSTU.TOKENS = []
    '''
    ||| Ascolta tutto il flusso di tokens e lo salva in TOKENS.
    '''
    while True:  
        TOKEN = await WORKER.HEAR()
        await WORKER.ECHO(TOKEN)
        if TOKEN == None:break
        TOKENS.append(TOKEN)
    
    
    
    await WORKER.FOREACH(TOKENS,INSTU)
    await WORKER.SPEAK('VALIDATOR',0)
    