import WebSocket, { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", socket => {
  socket.on("message", async raw => {
    const message = JSON.parse(raw.toString());
    if (message.type === "subscribe") {
      socket.send(JSON.stringify(await loadProjectEvents(message.projectId)));
    }
  });
});
