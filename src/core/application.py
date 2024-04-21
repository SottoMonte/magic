# CORE
from queue import Queue
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
import websockets
# CLI
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
import datetime
import inspect
# GUI
import flet as ft
# API
from fastapi import FastAPI
import uvicorn

import signal
import functools
import threading

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

connections = set()

async def handler(websocket, path):
        print(connections,path)
        async for msg in websocket:
            print(':>',msg)
            for ws in connections:
                asyncio.ensure_future(ws.send(msg))

API = FastAPI()

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    blu = "\x1b[34m"
    green = "\x1b[32m"
    cyan = "\x1b[36m"
    magenta = "\x1b[35m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] - %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: magenta + format + reset,
        logging.INFO: blu + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class mathemagic:
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
        #Log
        self.logger = logging.getLogger(self.identifier)
        logging.basicConfig(filename=f"examples/{self.identifier}.log",level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(CustomFormatter())
        self.logger.addHandler(handler)

    # Assegna il lavoro al lavoratore
    def JOB(self,job):
        lab = WORKER.MakeWorker(self,job)
        asyncio.get_event_loop().create_task(job(lab))
        #asyncio.get_event_loop().create_task(WORKER.HEAR(lab,{}))
        #self.workers[job.__name__] = WORKER.MakeWorker(self,job)
    # Avvia l'applicazione
    def RUN(self):
        # Avvia le interfacce del programma
        for key, interface in self.interfaces.items():
            match key:
                case INTERFACE.CLI:
                    self.JOB(interface)
                case INTERFACE.GUI:
                    #ft.app(target=interface)
                    pass
                case INTERFACE.API:
                    time.sleep(1)
                    loop = asyncio.get_event_loop()
                    config = uvicorn.Config(API, loop=loop, host="192.168.10.11", port=8400)
                    #loop.create_task(CLI(self))
                    server = uvicorn.Server(config)
                    #if 'CLI' in self._INTERFACE:loop.create_task(CLI(self))
                    loop.run_until_complete(server.serve())
                    #loop.create_task(server.serve())
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
        
        

async def BUILDER(worker,file):

    return None