#from multiprocessing import Process, Pipe
from dataclasses import dataclass
from threading import Thread
import os
import sys
import asyncio
import time
import datetime
from prompt_toolkit import print_formatted_text as print
from data import Metadata,VARIABLE,XML
from contextlib import suppress
#file
import aiofiles
# STATIC varibile
import functools
import inspect
# Publish-Subscribe
import redis.asyncio as redis

def static_vars(**kwargs):
    async def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate

'''
# -- WORKER -- [OPERATORS|PROPERTY-Characteristic|WORKER|METHODS|ATTRIBUTES,EVENTS]
# [STATI/EVENTS]: START,STARTING,WAIT,WAITING,END,ENDING,WORKING,WORK
# [ACTIONS]: HEAR,SPEAK
# [LOGIC]:= STATIC
# [DATA]: EVENTS,LOOP,OBJECTS
# iscrizzione-subisctrizzione,eventi
### Actions:(worker,args,kargs)
# gestisce il flusso del programma
'''

@dataclass(frozen=True)
class WORKER:
    identifier:Metadata
    job:Metadata
    events:Metadata
    app:Metadata
    tasks:Metadata
    
def MakeWorker(app,job):
    return WORKER(f"{app.identifier}.{job.__name__}",job,dict({}),app,[])

# Funzione che restituisce un decoratore che si occupa degli eventi e identità di una azione
def ACTION(argument=None,events=None):
    def decorator(function):
        print("INIZIO ACTION")
        async def wrapper(*arg, **kwargs):
            await asyncio.sleep(2)
            print("------>",*arg,argument,events)
            try:
                ss = []
                for x in arg[1:]:
                    print("-->>>",x)
                    ss.append(str(type(x)))
                print("####",ss)
                gg = argument(arg[0],ss)[0]
                if gg:
                    output = await function(*arg, **kwargs)
                    arg[0].SIGNAL(function.__name__)
                    if argument(arg[0],output)[0]:
                        return output
                    else:
                        print("errore output")
                else:
                    print("errore identita") 
            except Exception as e:
                print('Something went wrong.', e)
        return wrapper
    return decorator


# api basso livello per aggiungere callback
def CALL(self,FN):
    #print(self._LOOP)
    asyncio.get_event_loop().call_soon(FN,self)



# basso livello per aggiungere un callback a un determinato orario
def CALL_WHEN(self,FN,TIME:str,*ARGS,**KWARGS):
        timestamp = datetime.datetime.now()
        print(timestamp.time().hour,timestamp.time().minute)
        if (TIME != "") | (TIME == "NOW"):
            
            if TIME == "NOW": tt = timestamp.time()
            else: tt = datetime.datetime.strptime(TIME, '%H:%M')
            
            total = 0
            h =  tt.hour - timestamp.time().hour 
            m = tt.minute - timestamp.time().minute
            print(h,m)
            if h >= 0:
                total += h *3600    
                if m >= 0:
                    total += m *60
                    print(total)
                    current_time = asyncio.get_event_loop().time() + total
                    asyncio.get_event_loop().call_at(current_time,FN,self,*ARGS)
                else:
                    print("---------------------- SCADUTO!")
            else:
                print("----------------------  SCADUTO!")
        else:
            print("----------------------  SCADUTO!")


async def SIGNAL(self,event):
    self.app.GET().logger.info("Started Event %s",event)
    #print("ICASODSADSS",self.EVENTS.GET()[NAME])
    if event in self.events.GET():
        for item in self.events.GET()[event]:
            _ = await item[0](*item[1])
            #task = asyncio.get_event_loop().create_task(I[0](I[1]))
    self.app.GET().logger.info("Terminated Event %s",event)


def TASK(self,task):
    #tasks.append(loop.create_task(observe_changes(asyncio.sleep, shutdown_event)))
    asyncio.get_event_loop().create_task(task(self))


async def STOP(self):
        for key,task in self.tasks.GET().items():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task  # await for task cancellation
        #self.thread.
        #self.loop.GET().stop()
        #self.loop.GET().close()
        #self.loop.GET().call_soon(self.loop.GET().stop)

async def ECHO(worker,data):
    #worker.app.logger.info(f"{worker.identifier}: {data}")
    if type(data) == type('str'):
        print(data)
    else:
        print(str(data))


async def FOREACH(worker,data,fn,**constants):
    output = {'output':''}
    for idx,x in enumerate(data):
        if len(data) > idx+1:
            output = await fn(worker,index=idx,current=x,next=data[idx+1],**output,**constants)
        else:
            #output = await fn(worker,x,data[idx],output)
            output = await fn(worker,index=idx,current=x,next=data[idx],**output,**constants)
        

async def MATCH(worker,target,default,*cases):
    for case in cases:
        expression = case[0]
        block = case[1]
        if expression(worker,target)[0]:
            return await block(worker)
    return await default(worker)


async def BUILDER(worker,resource,mode,www=None):
    if mode == 'make':
        await aiofiles.os.makedirs(resource, exist_ok=True)
    elif mode == 'move':
        await aiofiles.os.replace(resource, www)
    elif mode == 'del':
        await aiofiles.os.remove(resource)
    elif mode == 'name':
        await aiofiles.os.rename(resource, www)


async def WRITER(worker,file,contents,mode='w'):
    '''async with aiofiles.open(file, mode) as handle:
            # write to the file
            await handle.write(contents)'''
    with open(file, mode) as f:
        f.write(contents)
    

#@data.METADATA(data.DATA(None,'STRING','b',(1,2)))
async def READER(worker,file,fn,mode="line"):
    with open(file, mode='r') as handle:
        data = handle.read()
        if mode == 'line':
            _ = await FOREACH(worker,data.splitlines(),fn)
        elif mode == 'char':
            _ = await FOREACH(worker,data,fn,file=file)
        else:
            _ = await fn(data)
    #pickled_object = pickle.dumps(obj)
    #unpacked_object = pickle.loads(r.get('some_key'))
    await SPEAK(worker,'LEXER::READER::FINISHED',worker.tasks.__name__)

def SUMMATION(worker,lower,upper,expression):
    sum = 0
    return sum

def TEST(worker,unit):
        tot = 0
        for test in unit:
            expected_result, function, input_value = test
            actual_result,actual_name,actual_data = function(worker,input_value)
            if actual_result != expected_result:
                worker.app.logger.error(f"{function.identifier}::{actual_name} did not pass the test with {actual_result} | Input[{input_value}] -> Output[{actual_data}]")
            else:
                tot += 1
                worker.app.logger.debug(f"{function.identifier}::{actual_name} passed the test with {actual_result} | Input[{input_value}] -> Output[{actual_data}]")
        if tot != len(unit):
            worker.app.logger.error(f"Passed only {tot}/{len(unit)} tests.")
        else:
            worker.app.logger.info(f"Passed all {tot}/{len(unit)} tests.")


async def NEW(worker,data):
    boolean = await worker.app.broker.exists(data.identifier)

    if not boolean:
        #print(f'{worker.app.identifier}.{data.identifier}',data.value)
        #await worker.app.broker.mset({f'{worker.app.identifier}.{data.identifier}': XML(worker,data)})
        #await worker.app.broker.rpush(data.identifier, *data.value)
        print(f"NEW::{data.identifier}",data.type,data.value)
        match data.type:
            case 'list':
                await worker.app.broker.rpush(data.identifier, *data.value)
            case 'string':
                await worker.app.broker.set(data.identifier, data.value)
            case 'set':
                await worker.app.broker.sset(data.identifier, data.value)
            case 'dict':
                #await worker.app.broker.mset(data.value)
                await worker.app.broker.hmset(data.identifier, data.value)
            case 'hash':
                await worker.app.broker.hmset(data.identifier, data.value)
            case _:
                print("ERRORE TIPO",data.type)
        
        #await SPEAK(worker,data.identifier,"event: new data")


async def SET(worker,identifier,value,de=None):
    boolean = await worker.app.broker.exists(identifier)
    if boolean:
        typ = await worker.app.broker.type(identifier)
        print(f"SET::{identifier}",typ)
        match typ.decode('ascii'):
            case 'list':
                #print('list')
                a = await worker.app.broker.rpush(identifier, value)
                return a
            case 'string':
                #print('string')
                await worker.app.broker.set(identifier, str(value))
            case 'set':
                #print('set')
                await worker.app.broker.sset(identifier, value)
            case 'dict':
                #print('dict')
                await worker.app.broker.mset(identifier,value)
            case 'hash':
                #print('hash')
                await worker.app.broker.hmset(identifier,value)
        await SPEAK(worker,identifier,"change event")
    else:
        await NEW(worker,de)

async def REM(worker,identifier,start=0,end=-1):
    if await worker.app.broker.exists(identifier):
        typ = await worker.app.broker.type(identifier)
        print(f"REM::{identifier}",typ)
        match typ.decode('ascii'):
            case 'list':
                #await worker.app.broker.lpop(identifier,2)
                a = await worker.app.broker.ltrim(identifier,start,end)
                return a
                #firma_funzione = inspect.signature(worker.app.broker.ltrim)
                #print(firma_funzione)
            case 'string':
                #print(dir(worker.app.broker))
                a = await worker.app.broker.delete(identifier)
                pass
            case 'set':       
                a = await worker.app.broker.delete(identifier)
                return a
            case 'dict':
                #await worker.app.broker.hdel(identifier)
                pass
            case 'hash':
                keys = await worker.app.broker.hkeys(identifier)
                for key in keys:
                    id = f"{identifier}.{key.decode('ascii')}"
                    #print(id)
                    boolean = await worker.app.broker.exists(id)
                    if boolean:
                        await REM(worker,id)
                await worker.app.broker.hdel(identifier,*[key.decode('ascii') for key in keys])

async def ADD(worker,identifier,value):
    if await worker.app.broker.exists(identifier):
        typ = await worker.app.broker.type(identifier)
        match typ.decode('ascii'):
            case 'list':
                await worker.app.broker.rpush(identifier, value)
            case 'string':
                await worker.app.broker.set(identifier, value)
            case 'set':
                await worker.app.broker.sadd(identifier, value)
            case 'dict':
                await worker.app.broker.mset({identifier: value})
            case 'hash':
                await worker.app.broker.hset({identifier: value})

async def GET(worker,identifier):
    boolean = await worker.app.broker.exists(identifier)
    print(f"GET::{identifier}")
    if boolean:
        typ = await worker.app.broker.type(identifier)
        
        match typ.decode('ascii'):
            case 'list':
                value = await worker.app.broker.lrange(identifier, 0, -1)
                return VARIABLE(worker,typ.decode('ascii'),identifier,[x.decode('ascii') for x in value])
            case 'string':
                value = await worker.app.broker.get(identifier)
                return VARIABLE(worker,typ.decode('ascii'),identifier,value.decode('ascii'))
            case 'set':
                await worker.app.broker.sadd(identifier, value)
            case 'dict':
                return await worker.app.broker.mget(identifier)
            case 'hash':
                value = await worker.app.broker.hgetall(identifier)
                return VARIABLE(worker,typ.decode('ascii'),identifier,{x.decode('ascii'):value[x].decode('ascii') for x in value})
    else:
        typ = await worker.app.broker.type(identifier)
        print(typ)
        return None
            
async def HEAR(worker,*channels):
    async def reader(channel: redis.client.PubSub):
        while True:
            await asyncio.sleep(0.1)
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message is not None:
                events = []
                data = message['data'].decode('ascii')
                pattern = message['channel'].decode('ascii')
                pchannel = message['pattern'].decode('ascii')
                if pattern in worker.events:
                    for event in worker.events[pattern]:
                        events.append(event(worker,data=data,channel=pchannel,pattern=pattern))
                    _ = await asyncio.gather(*events)
                elif pchannel in worker.events:
                    for event in worker.events[pchannel]:
                        events.append(event(worker,data=data,channel=pchannel,pattern=pattern))
                    _ = await asyncio.gather(*events)
                else:
                    print(f"(Reader) Message Received: {message}")
                

    async with worker.app.broker.pubsub() as pubsub:
        await pubsub.psubscribe(*channels)
        #if coroutine == None:
        #await pubsub.subscribe(**coroutine)
        future = asyncio.create_task(reader(pubsub))
        await future
        #await pubsub.psubscribe("tokens")

    '''
    while True:
    # Leggi i messaggi dallo stream
        messages = await worker.app.broker.xread({topic: "0"}, count=1)
            # Elabora i messaggi
        for _, message_list in messages:
            for message_id, message_data in message_list:
                #_ = await asyncio.gather(*worker.events[topic])
                events = []
                for event in worker.events[topic]:
                    events.append(event(worker,message_data[b'message'].decode('ascii')))

                _ = await asyncio.gather(*events)
                 
                #print(f"Message ID: {message_id}, Data: {message_data}")
                
                _ = await worker.app.broker.xdel(topic, message_id)
        await asyncio.sleep(0.1)'''
        

# Used for talk with other Workers
async def SPEAK(worker,key,value):
    #async with worker.app.broker.pubsub() as pubsub:
        #await worker.app.broker.publish(key, value)
    #asyncio.get_running_loop().create_task(worker.app.broker.publish(key, value))
    await worker.app.broker.publish(key, value)
    #await worker.app.broker.xadd(key, {'message': value},maxlen=10)
    #b = await worker.app.broker.xlen(key)
    #print(b)

# Server per aggiungere un evento 
async def EVENT(worker,event,coroutine):
    if event in worker.events:
        #isinstance(worker.events[event])
        #worker.events.ADD(None,{event:[(FN,ARGS)]})
        worker.events[event].append(coroutine)
    else:
        worker.events[event] = [coroutine]