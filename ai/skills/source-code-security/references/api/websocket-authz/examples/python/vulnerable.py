import json
import websockets

async def handler(socket):
    async for raw in socket:
        message = json.loads(raw)
        if message["type"] == "subscribe":
            events = await load_project_events(message["projectId"])
            await socket.send(json.dumps(events))
