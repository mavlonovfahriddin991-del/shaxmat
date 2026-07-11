# Fix app.js for deployment

d = open("c:/Users/MARUFXON/Desktop/12/app.js", "r", encoding="utf-8").read()

# 1. Fix WebSocket - add pathname for Render.com
old_ws = """function connectWebSocket(){
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  ws = new WebSocket(proto + "//" + host);"""

new_ws = """function connectWebSocket(){
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  const p = window.location.pathname.replace(/\\/+$/, "");
  ws = new WebSocket(proto + "//" + host + p);"""

d = d.replace(old_ws, new_ws)

# 2. Remove duplicate chat case
old_chat = """        case "chat":
      if(currentGameId === msg.gameId){
        addChatMessage(msg.from, msg.text);
      }
      break;
        case "chat":"""

new_chat = """        case "chat":"""

d = d.replace(old_chat, new_chat)

with open("c:/Users/MARUFXON/Desktop/12/app.js", "w", encoding="utf-8") as f:
    f.write(d)

print("Fixed app.js:", len(d), "chars")

# Verify
d2 = open("c:/Users/MARUFXON/Desktop/12/app.js", "r", encoding="utf-8").read()
chat_count = d2.count('case "chat"')
print('chat case count:', chat_count)
print('WebSocket path fix:', 'window.location.pathname' in d2)
