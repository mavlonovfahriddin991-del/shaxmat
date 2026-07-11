# Fix server.js for Render.com

d = open("c:/Users/MARUFXON/Desktop/12/server.js", "r", encoding="utf-8").read()

old = "const app = express();\nconst server = http.createServer(app);\nconst wss = new WebSocketServer({ server });"
new = "const app = express();\napp.set(\"trust proxy\", 1);\nconst server = http.createServer(app);\nconst wss = new WebSocketServer({ server });"
d = d.replace(old, new)

with open("c:/Users/MARUFXON/Desktop/12/server.js", "w", encoding="utf-8") as f:
    f.write(d)
print("server.js fixed")
