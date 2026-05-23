import json
import websockets

async def handler(socket):
    user = await authenticate_socket(socket.request_headers)
    async for raw in socket:
        message = json.loads(raw)
        if message["type"] == "subscribe":
            await assert_project_member(user.id, message["projectId"])
            events = await load_project_events(message["projectId"])
            await socket.send(json.dumps(events))
