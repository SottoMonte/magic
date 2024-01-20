#from multiprocessing import Process, Pipe

from threading import Thread
import os
import asyncio
import time
#import object
import datetime
from prompt_toolkit import print_formatted_text as print
import data
import logic
import object
from contextlib import suppress
#file
import aiofiles
# STATIC varibile
import functools


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
### Actions:(worker,args,kargs)
'''
class WORKER(object.OBJECT):
    
    job = data.variable(["<class 'str'>","<class 'list'>"],'job_worker',"")
    events = data.variable(["<class 'dict'>"],'worker.events',dict({}))
    loop = data.variable(["<class 'asyncio.unix_events._UnixSelectorEventLoop'>"],'worker.loop')
    thread = data.variable(["<class 'threading.Thread'>"],'worker.thread')
    app = data.variable(["<class 'application.mathmagic'>"],'worker.app')
    tasks = data.variable(["<class 'dict'>"],'worker.tasks',dict({}))

    def __init__(self,job,app):
        # trasforma gli attributa da attributi classe a di oggetto
        val = {
            'thread':Thread(target=self.MAIN,  args=()),
            'tasks':{"MAIN":job},
            'app':app,
            #'job':job,
        }

        for attr in dir(self):
            val_attr = getattr(self,attr)
            if type(val_attr) == type(data.variable()):
                if attr in val:
                    setattr(self,attr,data.variable(val_attr._TYPE,attr,val[attr]))
                else:
                    setattr(self,attr,data.variable(val_attr._TYPE,attr,val_attr._VALUE))
                #print(attr)
        # nuovo codice
        #self.thread = data.VARIABLe(["<class 'threading.Thread'>"],'thread',Thread(target=self.MAIN,  args=()))
        self.identifier = job.__name__
        #self.tasks.ADD(None,{"MAIN":job})
        #self.app.SET(None,app)
        #self.app = data.VARIABLe(["<class 'application.sloth'>"],'app',app)
        #self.job = data.VARIABLe(["<class 'str'>"],'job')
        
    def MAIN(self):
        self.app.GET().logger.info("Started worker %s",self.identifier)
        # Crea un nuovo loop
        #self.loop.SET(None,asyncio.new_event_loop())
        self.loop = data.variable(["<class 'asyncio.unix_events._UnixSelectorEventLoop'>"],'loop',asyncio.new_event_loop())
        loop = self.loop.GET()
        # Set loop for thread corrente        
        asyncio.set_event_loop(loop)
        # Avvia il loop eventi
        
        '''try:
            task = self.loop.GET().create_task(self.tasks.GET()['MAIN'](self))
            self.tasks.ADD(self,{"MAIN":task})
            self.loop.GET().run_forever()
        except KeyboardInterrupt:
            print("asdsad")
            pass
        except Exception as e:
            print(e)'''
        task = loop.create_task(self.tasks.GET()['MAIN'](self))
        self.tasks.ADD(self,{"MAIN":task})
        '''try:
            try:
            # Run the event loop
                loop.run_forever()
            finally:
                loop.close()
        except Exception as e:
            print(e)

        loop.close()'''
        def ask_exit():
            print("out")
        loop.run_forever()
        self.app.GET().logger.info("Terminated worker %s",self.identifier)

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
    '''
# Gestione
    ''' 

    async def SIGNAL(self,event):
        self.app.GET().logger.info("Started Event %s",event)
        #print("ICASODSADSS",self.EVENTS.GET()[NAME])
        if event in self.events.GET():
            for item in self.events.GET()[event]:
                _ = await item[0](*item[1])
                #task = asyncio.get_event_loop().create_task(I[0](I[1]))
        self.app.GET().logger.info("Terminated Event %s",event)

    # Server per aggiungere un evento 
    def EVENT(self,event,FN,*ARGS):
        self.events.ADD(None,{event:[(FN,ARGS)]})

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
    '''
# Communicazione
    ''' 
    async def HEAR(self):
        try:
            return await asyncio.wait_for(self.app.GET()._pipes[self.identifier].get(),1)
        except Exception as e:
            #print(f"Tempo scaduto ascolto {self.tasks.GET()['MAIN'].__name__}")
            return None
    
    # Used for talk with other Workers
    async def SPEAK(self,NAME,VALUE):
        await self.app.GET()._pipes[NAME].put(VALUE)

    #@ACTION(logic.EXPRESSION("SET",logic.EACH_t(logic.EQL,logic.TARGET,["<class 'str'>","<class 'data.VARIABLe'>"])))
    #@ACTION(logic.EXPRESSION("ECHO",logic.EACH_t(logic.EQL,["<class 'str'>"],logic.TARGET)),['SET'])
    async def ECHO(self,data):
        if type(data) == type('str'):
            print(data)
        else:
            print(str(data))

    '''
# Cicli
    '''    

    async def FOREACH(self,data,fn):
        # data[idx+1]
        '''for idx, x in enumerate(data):
            _ = await fn(x,0)'''
        end = 1
        dd = data
        '''for idx in range(0,len(data)+2):
            #print(data[start:])
            c = await fn(dd,end)
            print('[OUT]',c,dd[:c[1]])
            #len(data) > end and
            if c[0] != None:
                dd = dd.replace(dd[:c[1]], "", 1)'''
        #await asyncio.gather(foo(), bar())
        for idx,x in enumerate(data):
            if len(data) > idx+1:
                await fn(x,data[idx+1])
            else:
                await fn(x,data[idx])
        
                
            
            
            

    async def MATCH(self,target,default,*cases):
        for case in cases:
            if case[0] == target:
                return case[1]()
        return default

    async def BUILDER(self,resource,mode,www=None):
        if mode == 'make':
            await aiofiles.os.makedirs(resource, exist_ok=True)
        elif mode == 'move':
            await aiofiles.os.replace(resource, www)
        elif mode == 'del':
            await aiofiles.os.remove(resource)
        elif mode == 'name':
            await aiofiles.os.rename(resource, www)

    async def WRITER(self,file,mode):
        async with aiofiles.open('test_write.txt', mode='w') as handle:
            # write to the file
            await handle.write('Hello world')
    
    async def READER(self,file,fn,mode="line"):
        async with aiofiles.open(file, mode='r') as handle:
            data = await handle.read()
            if mode == 'line':
                _ = await self.FOREACH(data.splitlines(),fn)
            elif mode == 'char':
                _ = await self.FOREACH(data,fn)
            else:
                _ = await fn(data)