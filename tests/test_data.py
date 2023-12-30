import sys
sys.path.append('../sloth/core/')
import worker
import application
import asyncio



async def Test(worker:worker):
    
    pass

if __name__ == "__main__":
    app = application.sloth("example.cli",sys.argv,{'CLI':application.CLI})
    app.JOB(Test)
    app.RUN()