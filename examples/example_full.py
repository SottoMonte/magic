# Import
import sys
sys.path.append('src/core/')
sys.path.append('src/ide/')
import worker
import application
import asyncio
import ide
import flet as ft
import toml
import gui
# test
async def Test(worker:worker):
    
    pass

# main
if __name__ == "__main__":
    app = application.framework('hub.cloud',sys.argv,{application.INTERFACE.GUI:gui.main})
    #app.JOB(Test)
    app.RUN()