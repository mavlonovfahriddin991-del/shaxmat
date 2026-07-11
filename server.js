const express = require("express");
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
});

app.use(express.static(path.join(__dirname, "./")));

const users = new Map();
const games = new Map();

function broadcastUsers() {
  const online = [];
  for (const [name, data] of users) {
    if (data.ws.readyState === 1) online.push(name);
  }
  const msg = JSON.stringify({ type: "users", list: online });
  for (const [, data] of users) {
    if (data.ws.readyState === 1) data.ws.send(msg);
  }
}

function initialPieces() {
  return {
    0: "\u265c", 1: "\u265e", 2: "\u265d", 3: "\u265b", 4: "\u265a", 5: "\u265d", 6: "\u265e", 7: "\u265c",
    8: "\u265f", 9: "\u265f", 10: "\u265f", 11: "\u265f", 12: "\u265f", 13: "\u265f", 14: "\u265f", 15: "\u265f",
    48: "\u2659", 49: "\u2659", 50: "\u2659", 51: "\u2659", 52: "\u2659", 53: "\u2659", 54: "\u2659", 55: "\u2659",
    56: "\u2656", 57: "\u2658", 58: "\u2657", 59: "\u2655", 60: "\u2654", 61: "\u2657", 62: "\u2658", 63: "\u2656"
  };
}

wss.on("connection", (ws) => {
  let currentUser = null;

  ws.on("message", (raw) => {
    let msg;
    try { msg = JSON.parse(raw); } catch { return; }

    switch (msg.type) {
      case "register": {
        const name = msg.username?.trim();
        if (!name || name.length < 2) {
          ws.send(JSON.stringify({ type: "error", text: "Ism kamida 2 ta belgi" }));
          return;
        }
        if (users.has(name)) {
          ws.send(JSON.stringify({ type: "error", text: "Bu nom band" }));
          return;
        }
        currentUser = name;
        users.set(name, { ws, lastSeen: Date.now() });
        ws.send(JSON.stringify({ type: "registered", username: name }));
        broadcastUsers();
        break;
      }

      case "heartbeat": {
        if (currentUser && users.has(currentUser)) {
          users.get(currentUser).lastSeen = Date.now();
        }
        break;
      }

      case "sendInvite": {
        if (!currentUser) return;
        const target = msg.target;
        if (!users.has(target)) {
          ws.send(JSON.stringify({ type: "error", text: "Foydalanuvchi topilmadi" }));
          return;
        }
        const gameId = "g_" + Date.now() + "_" + Math.random().toString(36).slice(2, 8);
        const game = {
          id: gameId,
          white: currentUser,
          black: target,
          pieces: initialPieces(),
          turn: "white",
          status: "pending",
          lastMove: Date.now()
        };
        games.set(gameId, game);

        const targetData = users.get(target);
        if (targetData.ws.readyState === 1) {
          targetData.ws.send(JSON.stringify({
            type: "invite",
            gameId,
            from: currentUser
          }));
        }

        ws.send(JSON.stringify({
          type: "inviteSent",
          gameId,
          target
        }));
        break;
      }

      case "acceptInvite": {
        if (!currentUser) return;
        const game = games.get(msg.gameId);
        if (!game) return;
        game.status = "active";
        games.set(msg.gameId, game);

        const whiteData = users.get(game.white);
        const blackData = users.get(game.black);
        const notify = JSON.stringify({
          type: "gameStart",
          gameId: msg.gameId,
          pieces: game.pieces,
          turn: game.turn,
          white: game.white,
          black: game.black,
          yourColor: "white"
        });
        const notify2 = JSON.stringify({
          type: "gameStart",
          gameId: msg.gameId,
          pieces: game.pieces,
          turn: game.turn,
          white: game.white,
          black: game.black,
          yourColor: "black"
        });
        if (whiteData?.ws.readyState === 1) whiteData.ws.send(notify);
        if (blackData?.ws.readyState === 1) blackData.ws.send(notify2);
        break;
      }

      case "declineInvite": {
        if (!currentUser) return;
        const game = games.get(msg.gameId);
        if (game) game.status = "declined";
        const fromData = users.get(game?.white);
        if (fromData?.ws.readyState === 1) {
          fromData.ws.send(JSON.stringify({
            type: "inviteDeclined",
            gameId: msg.gameId
          }));
        }
        break;
      }

      case "move": {
        if (!currentUser) return;
        const game = games.get(msg.gameId);
        if (!game) return;
        game.pieces = msg.pieces;
        game.turn = msg.turn;
        game.lastMove = Date.now();

        const whiteData = users.get(game.white);
        const blackData = users.get(game.black);
        const notify = JSON.stringify({
          type: "gameUpdate",
          gameId: msg.gameId,
          pieces: game.pieces,
          turn: game.turn
        });
        if (whiteData?.ws.readyState === 1) whiteData.ws.send(notify);
        if (blackData?.ws.readyState === 1) blackData.ws.send(notify);
        break;
      }

      case "chatMsg": {
        if (!currentUser) return;
        const game = games.get(msg.gameId);
        if (!game) return;
        const whiteData = users.get(game.white);
        const blackData = users.get(game.black);
        const chatNotify = JSON.stringify({
          type: "chat",
          gameId: msg.gameId,
          from: currentUser,
          text: msg.text
        });
        if (whiteData?.ws.readyState === 1) whiteData.ws.send(chatNotify);
        if (blackData?.ws.readyState === 1) blackData.ws.send(chatNotify);
        break;
      }

      case "leaveGame": {
        if (!currentUser) return;
        const game = games.get(msg.gameId);
        if (!game) return;
        game.status = "ended";
        const whiteData = users.get(game.white);
        const blackData = users.get(game.black);
        const notify = JSON.stringify({
          type: "gameEnded",
          gameId: msg.gameId,
          by: currentUser
        });
        if (whiteData?.ws.readyState === 1) whiteData.ws.send(notify);
        if (blackData?.ws.readyState === 1) blackData.ws.send(notify);
        break;
      }
    }
  });

  ws.on("close", () => {
    if (currentUser) {
      users.delete(currentUser);
      broadcastUsers();
    }
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log("Server ishga tushdi: http://localhost:" + PORT);
});
