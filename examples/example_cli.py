# Import
import sys
sys.path.append('../sloth/core/')
import application

#Consumer
async def Consumer(worker):
    while True:
        TOKEN = await worker.HEAR()
        if TOKEN != None:
            _ = await worker.ECHO("Consumer Talk:"+TOKEN)
# Consumer
async def Consumer2(worker):
    while True:
        TOKEN = await worker.HEAR()
        if TOKEN != None:
            _ = await worker.ECHO("Consumer Talk:"+TOKEN)
# Main
if __name__ == "__main__":
    app = application.sloth("example.cli",sys.argv,{'CLI':application.CLI})
    app.JOB(Consumer)
    app.JOB(Consumer2)
    app.RUN()