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

    def ACTION(events=None,bond=None):
        def decorator(function):
            async def wrapper(*args, **kwargs):
                try:
                    #print(*args,argument,events)
                    output = None
                    worker = None
                    target = None
                    where = 0
                    for arg in args:
                        if str(type(arg)).find('worker.WORKER') != -1:
                            worker = arg
                            if where == 0:
                                target = args[1]
                            else:target = args[0]
                            where += 1
                    # run function
                    if bond != None:
                        check = bond(worker,args[2:])
                        if check[0]:
                            worker.app.GET().logger.debug(f"{function.__name__} pass the bound {check[1]} with {bond} and data := {check[2]}")
                            output = function(*args, **kwargs)
                        else:
                            worker.app.GET().logger.error(f"{function.__name__} Not pass the bound {check[1]} with {bond} and data := {check[2]}")
                    else:
                        output = function(*args, **kwargs)
                    # run event
                    if worker != None:
                        _ = await worker.SIGNAL(function.__name__)
                    return output
                except Exception as e:
                    worker.app.GET().logger.error(f"the {function.__name__} raise Exception {e}")
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