import sys
sys.path.append('../sloth/core/')
import worker
import application
import asyncio
import logic



async def Test(worker:worker):

    pass

if __name__ == "__main__":
    cc = logic.EXPRESSION("cc",logic.EQL('a',logic.TARGET))

    cc(None,B="ciao")