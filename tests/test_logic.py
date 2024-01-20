import sys
sys.path.append('src/core/')
import worker
import application
import asyncio
import logic

async def Tester(worker):
    test = logic.TEST(
        (logic.eql,[1,1],True),
    )

    print(test.check(worker))

if __name__ == "__main__":
    

    app = application.sloth("example.cli",sys.argv,{})
    app.JOB(Tester)
    app.RUN()

    