# Import
import sys
sys.path.append('src/core/')
import application
import asyncio
import logic

#Consumer
async def Consumer(worker):
    while True:
        TOKEN = await worker.HEAR()
        if TOKEN != None:
            _ = await worker.ECHO("Consumer Talk:"+TOKEN)
# zz
async def Task_1(worker):
    await worker.ECHO("True")

    return None
            
    
    

# Consumer
async def Consumer2(worker):
    await worker.job.SET(worker,"settato")
    await worker.ECHO(worker.job)
    worker.TASK(Task_1)
    tt = logic.expression("logica",logic.eql(1,logic.TARGET))
    qq = logic.expression("conta",logic.count("@A@@",'@',2))
    gg = logic.expression("orr",logic.OR(logic.count("@A@@",'@','cc'),logic.eql(1,logic.TARGET)))
    await worker.ECHO(tt)
    await worker.ECHO(tt(worker,1))
    await worker.ECHO(qq)
    await worker.ECHO(qq(worker))

    await worker.ECHO(gg)
    await worker.ECHO(gg(worker,2,cc=2))
    
    
    
# Main
if __name__ == "__main__":
    app = application.mathemagic("example.cli",sys.argv,{application.INTERFACE.CLI:application.CLI})
    app.JOB(Consumer)
    app.JOB(Consumer2)
    app.RUN()