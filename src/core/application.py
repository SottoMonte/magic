# CORE
from queue import Queue
import asyncio
import sys
import time
import worker
import object
import data
import logging
from enum import Enum
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

class mathmagic(object.OBJECT):
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
        self._interfaces = interfaces
        self._platform = platform
        self._target = target
        self._type = type
        self._args = args
        self._workers = dict()
        self._pipes = dict()

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
        self._workers[job.__name__] = worker.WORKER(job,self)
        self._pipes[job.__name__] = asyncio.Queue()
    # Avvia l'applicazione
    def RUN(self):
        # Avvia le interfacce del programma
        for key, interface in self._interfaces.items():
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
        
        def ask_exit(signame, loop):
            async def Task_1(worker):
                worker.loop.GET().stop()
                pass
            #print("got signal %s: exit" % signame)
            #print(threading.current_thread().name)
            #loop.stop()
            for key, worker in self._workers.items():
                
                future = asyncio.run_coroutine_threadsafe(Task_1(worker), worker.loop.GET())
        
        # Avvia i lavoratori
        for key, worker in self._workers.items():
            worker.thread.GET().start()
        # Add event signal
        '''for signame in {'SIGINT', 'SIGTERM'}:
            asyncio.get_event_loop().add_signal_handler(
                    getattr(signal, signame),
                    functools.partial(ask_exit, signame, asyncio.get_event_loop()))'''
        
        time.sleep(1)
        for key, worker in self._workers.items():
            loop = worker.loop.GET()
            for signame in {'SIGINT', 'SIGTERM'}:
                loop.add_signal_handler(
                    getattr(signal, signame),
                    functools.partial(ask_exit, signame, loop))
        
        # Attende i lavoratori
        #for key, worker in self._workers.items():
        #  worker.thread.GET().join()
        '''try:
            for key, worker in self._workers.items():
                worker.thread.GET().join()
        except KeyboardInterrupt:
            print('\nExit with Ctrl + C')'''
        if 'GUI' in self._interfaces:
            self.logger.info("Started worker GUI")
            ft.app(target=self._interfaces['GUI'])
            self.logger.info("Terminated worker GUI")

# Show data target    
async def DATA(self:worker.WORKER):
    print_formatted_text(f"{'Type':#^40.40}:{'Identifier':#^15.15} = {'Value':#^30.30}")
    for attr in dir(self):
        val_attr = getattr(self,attr)
        if type(val_attr) == type(self.job):
            print_formatted_text(repr(val_attr))
    return None

# Command line interface
async def CLI(self:worker.WORKER):
    # Local variable
    target = self
    cmd = ""
    root = "_:> "
    mode = 'None'
    modes = ['None','Talk','Terminal','Edit','Interpreter','Debug']
    keywords = ['help', 'workers', 'exit','actions','action'] + modes
    # Style
    style = Style.from_dict({
        'rprompt': 'bg:#4d90fe #ffffff',
    })
    # Create some history first.
    history = InMemoryHistory()
    for keyword in keywords:
        history.append_string(keyword)

    # Create Prompt.
    session = PromptSession(
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
    )

    # Builder Toolbar
    def toolbar(self):
        now = datetime.datetime.now()
        return f"Target: {target.identifier} | Workers: {len(self.app.GET()._workers)} | Mode: {mode} | Time:{now.hour}:{now.minute}:{now.second} | [Tab] Suggestion [Up Arrow] History [F1] Help [Enter] Send [Ctrl + C] Exit"

    # Run loop
    while cmd != "exit":
        try:
            cmd = await session.prompt_async(root, style=style, rprompt="", completer=WordCompleter(keywords), bottom_toolbar=toolbar(self), refresh_interval=0.1)
            match cmd:
                case 'change':
                    lw = []
                    for wor in self.app.GET()._workers:
                        lw.append(wor)
                    value = await session.prompt_async(root, rprompt='<str>', completer=WordCompleter(lw))
                    target = self.app.GET()._workers[value]
                case 'action':
                    actions = []
                    parameters = None
                    action_target = None
                    for attr in dir(target):
                        if attr.isupper():
                            actions.append(attr)
                    action = await session.prompt_async(root, rprompt="Action", completer=WordCompleter(actions))
                    if action in dir(target):
                            action_target = getattr(self,action)
                            parameters = inspect.signature(action_target).parameters
                    if len(parameters) != 0:
                        value = await session.prompt_async(root, rprompt=str(parameters), completer=WordCompleter(keywords))
                        _ = await action_target(self.job)
                    else:
                        _ = await action_target()
                case 'actions':
                    for attr in dir(self):
                        if attr.isupper():
                            val_attr = getattr(self,attr)
                            print_formatted_text(attr,inspect.signature(val_attr))
                case 'talk':
                    value = await session.prompt_async(root, rprompt='<str>', completer=WordCompleter(keywords))
                    _ = await self.SPEAK('Consumer',value)
                case 'set':
                    text = await session.prompt_async(root, rprompt=self.job.TYPE(self), completer=WordCompleter(keywords), bottom_toolbar=toolbar(self), refresh_interval=0.1)
                    _ = await target.job.SET(self,text)
                case 'cancel':
                    workers = self.app.GET()._workers
                    for worker in workers:
                        if worker != 'CLI':
                            for key,task in workers[worker].tasks.GET().items():
                                task.cancel()
                            #workers[worker].loop.GET().call_later(0,workers[worker].loop.GET().stop())
                    
                    
                    for worker in workers:
                        #workers['CLI'].loop.GET().call_later(0,workers['CLI'].loop.GET().stop())
                        workers[worker].loop.GET().call_later(0,workers[worker].loop.GET().stop())
                    print('Done')
                case 'exit':
                    #_ = await self.app.GET()._workers['Consumer'].STOP()
                    workers = self.app.GET()._workers
                    for worker in workers:
                        workers[worker].loop.GET().stop()
                case 'help':
                    print('MODE:[workers]\n Sub:[Debug:data,event]')
                case 'None':
                    root = '_:> '
                    mode = 'None'
                case 'Debug':
                    root = root.replace(f"({mode}) ", '', 1)
                    root = '(Debug) ' + root
                    mode = 'Debug'
                case 'Edit':
                    root = root.replace(f"({mode}) ", '', 1)
                    root = '(Edit) ' + root
                    mode = 'Edit'
                case 'data':
                    if mode == 'Debug':
                        _ = await DATA(target)
                        self.EVENT('SET',DATA,target)
                    else:
                        self.app.GET().logger.warning('need debug mode !, you are currently in mode %s',mode)
                case 'workers':
                    for worker in self.app.GET()._workers:
                        print(worker)
                case _:
                    print('Bad command - ',cmd)
        except (EOFError,KeyboardInterrupt):
            async def Task_1(worker):
                worker.loop.GET().stop()
                pass
            for key, worker in  self.app.GET()._workers.items():
                future = asyncio.run_coroutine_threadsafe(Task_1(worker), worker.loop.GET())
            cmd = "exit"
