import sys
sys.path.append('src/core/')
import data
import worker as WORKER
import logic
import application

# Publish-Subscribe
import aiopubsub
import asyncio

async def on_trade(key: aiopubsub.Key, trade) -> None:
    print(f'Processing trade = {trade}  with key = {key}.',id(asyncio.get_event_loop()))

async def Test(worker:WORKER.WORKER):

    await WORKER.HEAR(worker,on_trade)

    a = data.DATA(worker,'STRING','a',[1,2,3,4])
    b = data.DATA(worker,'STRING','b',(1,2))

    
    
    coppia = data.DATA(worker,'INTEGER','coppia',{'x':0,'y':0})

    await WORKER.SPEAK(worker,'Test',data.XML(worker,coppia))

    await WORKER.ECHO(worker,data.STRING(worker,coppia))

async def Test2(worker:WORKER.WORKER):
    
    await WORKER.SPEAK(worker,'Test',"luna piena")


if __name__ == "__main__":
    app = application.mathemagic("data.test",sys.argv,{})
    app.JOB(Test)
    app.JOB(Test2)
    app.RUN()