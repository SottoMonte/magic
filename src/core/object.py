from sys import getsizeof
#import numpy as np
import time
import inspect
import os
import asyncio
import logic

class OBJECT:
    '''
    ||| -- OBJECT -- [OPERATORS|PROPERTY-Characteristic|WORKER|METHODS|ATTRIBUTES,EVENTS]
    |||[DATA]: OPERATORS,
    |||[ACT]: DECORETOR_METHOD,CHECK
    |||[LOGIC]:TEST,EXECUTABLE
    - l'Identità - è la proprietà di un oggetto di distinguersi dagli altri ed è rappresentata dal suo nome;
    - lo Stato - che è costituito dai dati associati a un oggetto, ed è rappresentato attraverso variabili associate a quell'oggetto;
    - il Comportamento - è descritto attraverso metodi che evocano le azioni che può compiere quell'oggetto.
    '''

    identifier = None
    operators = None
    
    # identity è la proprietà di un oggetto di distinguersi dagli altri
    Identity = logic.EXPRESSION('IDENTITY',logic.EQL(True,True))
    # un oggetto preposto alla creazione di altri oggetti.
    Factory = None
    # un oggetto che rappresenta l'unica istanza di una classe nell'esecuzione di un programma.
    Singleton = None
    # un oggetto con un solo metodo che agisce come una funzione
    Functor = None
    # un metaobject specializzato da cui altri oggetti possono venir creati attraverso la copia.
    Metaobject = None
    # un metaobject specializzato da cui altri oggetti possono venir creati attraverso la copia.
    Prototype = None

    def CHECK(self,NAME,ARGS):
        if NAME in self.PROPERTY:
            for CHECK in self.PROPERTY[NAME]:
                result = CHECK.VERIFIED()
                if result[0] == True: pass
                else: print(f"Errore:{result[1]}|TARGET:{CHECK._TARGET}|TEST:{CHECK._TEST}")

    def EVENT(self,NAME):
        try:
            self.WORKER._SIGNAL(NAME)
            pass
        except KeyError as ke:
            pass
    
    # funzione che restituisce un decoratore che si occupa degli eventi e identità di una azione
    def ACTION_ASYNC(argument=None,events=None):
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

    def ACTION(argument=None,events=None):
        def decorator(function):
            async def wrapper(*args, **kwargs):
                #print(*args,argument,events)
                try:
                    worker = None
                    for arg in args:
                        if str(type(arg)).find('worker.WORKER') != -1:
                            worker = arg
                    # run function
                    output = function(*args, **kwargs)
                    # run event
                    if worker != None:
                        _ = await worker.SIGNAL(function.__name__)
                    return output
                except Exception as e:
                    print('Something went wrong.', e)
            return wrapper
        return decorator

    def METHOD(METHOD):
        def CALL(self,*ARGS):
            self.CHECK(METHOD.__name__,ARGS)
            OUT = METHOD(self,*ARGS)
            self.EVENT(METHOD.__name__)
            print("IN|ARGS:", ARGS,"")
            print(self.PROPERTY,self.OPERATORS)
            return OUT
        return CALL
    

TEST = logic.TEST(
    (None,True,"=="),
)