# Fix server.js for Render.com WebSocket properly
d = open("c:/Users/MARUFXON/Desktop/12/server.js", "r", encoding="utf-8").read()

# Replace the entire WebSocket init with a proper one
old = """const express = require("express");
const http = require("http");
const { WebSocketServer } = require("ws");
const path = require("path");

const app = express();
app.set("trust proxy", 1);
const server = http.createServer(app);
const wss = new WebSocketServer({ server });"""

new = """const express = require("express");
const http = require("http");
const { WebSocketServer } = require("ws");
const path = require("path");

const app = express();
app.set("trust proxy", 1);
const server = http.createServer(app);

// WebSocket - handle upgrade ourselves to avoid conflict
const wss = new WebSocketServer({ noServer: true });

server.on("upgrade", function upgrade(request, socket, head) {
  // Accept all WebSocket connections
  wss.handleUpgrade(request, socket, head, function done(ws) {
    wss.emit("connection", ws, request);
  });
});"""

d = d.replace(old, new)

with open("c:/Users/MARUFXON/Desktop/12/server.js", "w", encoding="utf-8") as f:
    f.write(d)
print("server.js fixed with proper WebSocket upgrade handling")
