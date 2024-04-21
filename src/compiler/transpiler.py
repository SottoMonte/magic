import sys
import os
import asyncio
sys.path.append('src/generator/')
import python
'''
# GENERATOR
# BUILDER
# TRANSLATOR
'''
async def TRANSLATOR(worker):
    argv = worker.app.GET()._args

    ttt = None
    source = ""
    tabulation = ""
    '''
    ||| Ascolta tutto il flusso fino a true
    '''
    while True:  
        TOKEN = await worker.HEAR()
        #await worker.ECHO(TOKEN)
        if TOKEN == True:break
        ttt = TOKEN

    for x in ttt:
        target = ttt[x]
        ty = ttt[x].type
        match ty:
            case python.INTEGER.__name__:
                source += python.INTEGER(target) + '\n'
            case python.STRING.__name__:
                source += python.STRING(target) + '\n'
            case "FN":
                source += python.CALL(target) + '\n'

    #await worker.ECHO(source)
    await worker.WRITER('target.py',source)
    '''
    ||| Errors - Requirements
    '''
    if '-compiled' in argv and '-interpreted' not in argv:
        worker.app.GET().logger.debug(f"file '{argv[0]}' has been compiled")
        pass
    elif '-compiled' not in argv and '-interpreted' in argv:
        
        stream = os.popen('python3 target.py')
        output = stream.read()

        worker.app.GET().logger.debug(f"file '{argv[0]}' has been interpreted Output:\n{output}")
        pass
    else:
        worker.app.GET().logger.error("enter one between '-compiled' and '-interpreted' as arguments")
        pass