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

class WORKER(object.OBJECT):
    '''
    ||| -- WORKER -- [OPERATORS|PROPERTY-Characteristic|WORKER|METHODS|ATTRIBUTES,EVENTS]
    |||[STATI/EVENTS]: START,STARTING,WAIT,WAITING,END,ENDING,WORKING,WORK
    |||[ACTIONS]: HEAR,SPEAK
    |||[LOGIC]:= STATIC
    |||[DATA]: EVENTS,LOOP,OBJECTS
    '''

    '''
    |||[DATA]
    '''
    job = data.VARIABLE(["<class 'str'>"],[1,2,3])
    events = data.VARIABLE(["<class 'list'>"],{})
    loop = data.VARIABLE(["<class 'asyncio.unix_events._UnixSelectorEventLoop'>"])
    thread = data.VARIABLE(["<class 'threading.Thread'>"])
    app = data.VARIABLE(["<class 'application.sloth'>"])
    tasks = data.VARIABLE(["<class 'function'>"],{})

    def __init__(self,job,app):
        # trasforma gli attributa da attributi classe a di oggetto
        for attr in dir(self):
            val_attr = getattr(self,attr)
            if type(val_attr) == type(data.VARIABLE()):
                setattr(self,attr,data.VARIABLE(val_attr._TYPE,val_attr._VALUE,attr))
                #print(attr)
        # nuovo codice
        self.thread = data.VARIABLE(["<class 'threading.Thread'>"],Thread(target=self.MAIN,  args=()),'thread')
        self.identifier = job.__name__
        self.tasks.ADD(None,{"MAIN":job})
        #self.app.SET(None,app)
        self.app = data.VARIABLE(["<class 'application.sloth'>"],app,'app')
        self.job = data.VARIABLE(["<class 'str'>"],[1,2,3],'job')
        
        
    '''
    |||[LOGIC]
    '''
    '''
    ||| [METHOD]
    '''
    def MAIN(self):
        self.app.GET().logger.info("Started worker %s",self.identifier)
        # Crea un nuovo loop
        #self.loop.SET(None,asyncio.new_event_loop())
        self.loop = data.VARIABLE(["<class 'asyncio.unix_events._UnixSelectorEventLoop'>"],asyncio.new_event_loop(),'loop')
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
        loop.run_forever()
        self.app.GET().logger.info("Terminated worker %s",self.identifier)

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
    
    # Funzione che restituisce un decoratore che si occupa degli eventi e identità di una azione
    def ACTION(argument=None,events=None):
        def decorator(function):
            async def wrapper(*arg, **kwargs):
                print("INIZIO ACTION")
                print(*arg,argument,events)
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
                print("FINE ACTION")
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
    |||[ACTION]
    '''
    
    def TASK(self,task):
        asyncio.get_event_loop().create_task(task(self))
    
    async def aaa(self):
        workers = self.app.GET()._workers
        for worker in workers:
            #workers['CLI'].loop.GET().call_later(0,workers['CLI'].loop.GET().stop())
            workers[worker].loop.GET().call_later(0,workers[worker].loop.GET().stop())

    async def STOP(self):
        for key,task in self.tasks.GET().items():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task  # await for task cancellation
        #self.thread.
        #self.loop.GET().stop()
        #self.loop.GET().close()
        #self.loop.GET().call_soon(self.loop.GET().stop)
    
    async def HEAR(self):
        try:
            return await asyncio.wait_for(self.app.GET()._pipes[self.identifier].get(),1)
        except Exception as e:
            #print(f"Tempo scaduto ascolto {self.tasks.GET()['MAIN'].__name__}")
            return None
    
    # Used for talk with other Workers
    async def SPEAK(self,NAME,VALUE):
        await self.app.GET()._pipes[NAME].put(VALUE)

    #@ACTION(logic.EXPRESSION("SET",logic.EACH_t(logic.EQL,logic.TARGET,["<class 'str'>","<class 'data.VARIABLE'>"])))
    #@ACTION(logic.EXPRESSION("ECHO",logic.EACH_t(logic.EQL,["<class 'str'>"],logic.TARGET)),['SET'])
    async def ECHO(self,data):
        if type(data) == type('str'):
            print(data)
        else:
            print(data.GET())

    async def FOR(self,data,fn):
        for x in data.GET():
            fn(x)