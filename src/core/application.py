# CORE
import toml
import asyncio
import sys
import time
import worker as WORKER
import data
import logging
from enum import Enum
# Publish-Subscribe
import redis.asyncio as redis
#import redis
import datetime
import inspect
# GUI
import flet as ft
# API
from fastapi import FastAPI
import uvicorn

import signal
import functools

class INTERFACE(Enum):
    API = 1
    CLI = 2
    GUI = 3

class PLATFORM(Enum):
    WEB = 1
    NATIVE = 2

class TARGET(Enum):
    MOBILE = 1
    BROWSER = 2
    DESKTOP = 3
    SERVER = 4

class TYPE(Enum):
    INTERPRETED = 1
    COMPILED = 2
    HYBRID = 3

class LANGUAGES(Enum):
    PHP = 1
    PYTHON = 2
    RUST = 3
    C = 4
    JAVASCRIPT = 5
    GO = 6

class DATABASE(Enum):
    SQL = 1

class FRAMEWORK(Enum):
    FLUTTER = 1
    GTK4 = 2
    LARAVEL = 3
    PANDA = 4

#INTERFACE = {'API':'API','CLI':'CLI','GUI':'GUI'}
#PLATFORM = {'WEB':'WEB','NATIVE':'NATIVE'}
#TARGET = {'MOBILE':'MOBILE','BROWSER':'BROWSER','DESKTOP':'DESKTOP','SERVER':'SERVER'}
#TYPE = {'INTERPRETED':'INTERPRETED', 'COMPILED':'COMPILED', 'HYBRID':'HYBRID'}
#LANGUAGES = {'PHP','PYTHON','RUST','SQL','C','JAVASCRIPT','GO'}
#FRAMEWORK = {'FLUTTER','GTK4','LARAVEL','PANDA'}

class framework:
    def __init__(
            self, 
            identifier:str,
            args:tuple = (),
            interfaces:dict = {},
            platform:str = PLATFORM.NATIVE,
            target:str = TARGET.DESKTOP,
            type:str = TYPE.INTERPRETED,
    ) -> None:
        # Inizializza gli attributi dell'oggetto
        self.identifier = identifier
        self.interfaces = interfaces
        self.platform = platform
        self.target = target
        self.type = type
        self.args = args
        self.workers = dict()
        self.broker = redis.from_url("redis://localhost:6379")
        self.data = dict({})

    '''
    ||| Assegna un lavoratore
    '''
    def JOB(self,job):
        lab = WORKER.MakeWorker(self,job)
        asyncio.get_event_loop().create_task(job(lab))
    '''
    ||| Avvia applicazione
    '''
    def RUN(self):
        # Avvia le interfacce del programma
        for key, interface in self.interfaces.items():
            match key:
                case INTERFACE.CLI:
                    self.JOB(interface)
                case INTERFACE.GUI:
                    ft.app(interface)
                    pass
                case INTERFACE.API:
                   pass
                case _:
                    print(f"Errore generico non esiste nessuna interfaccia {key}")
        
        try:
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            e_type = type(e).__name__
            e_file = e.__traceback__.tb_frame.f_code.co_filename
            e_line = e.__traceback__.tb_lineno

            e_message = str(e)

            print(f'exception type: {e_type}')

            print(f'exception filename: {e_file}')

            print(f'exception line number: {e_line}')

            print(f'exception message: {e_message}')
        except KeyboardInterrupt:
            print("Ctrl + C")