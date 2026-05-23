import WebSocket, { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", async (socket, req) => {
  const user = await authenticateUpgrade(req);
  socket.on("message", async raw => {
    const message = JSON.parse(raw.toString());
    if (message.type === "subscribe") {
      await assertProjectMember(user.id, message.projectId);
      socket.send(JSON.stringify(await loadProjectEvents(message.projectId)));
    }
  });
});
