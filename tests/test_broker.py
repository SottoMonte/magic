# Import
import sys
import asyncio
sys.path.append('src/core/')
import application
import logic
sys.path.append('src/analyzer/')
import lexical
import syntax
import semantic
sys.path.append('src/compiler/')
import transpiler

import redis.asyncio as redis

STOPWORD = "STOP"


async def reader(channel: redis.client.PubSub):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
        if message is not None:
            print(f"(Reader) Message Received: {message}",type(message['data']))
            if message["data"].decode() == STOPWORD:
                print("(Reader) STOP")
                break


async def run(f):
    r = f.app.broker

    async with r.pubsub() as pubsub:
        await pubsub.subscribe("channel:1", "channel:2")

        future = asyncio.create_task(reader(pubsub))

        await r.publish("channel:1", "Hello")
        await r.publish("channel:2", "World")
        #await r.publish("channel:1", STOPWORD)

        #await future
    


# Main
if __name__ == "__main__":
    app = application.mathemagic("language.mathemagic",sys.argv,{})
    app.JOB(run)
    app.RUN()