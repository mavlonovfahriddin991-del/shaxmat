# patch all files at once

import sys, os

SRC = "c:/Users/MARUFXON/Desktop/12"
DST = "c:/Users/MARUFXON/Desktop/12"

# ==================== 1. APP.JS - add timer + update enterGame/leaveGame ====================
with open(SRC + "/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# Add timer state variables after let pieces = {}
old_timer_state = """let currentUser = null;
let mode = null;
let myColor = "white";
let opponentName = "Kompyuter";
let turn = "white";
let selected = null;
let currentGameId = null;"""

new_timer_state = """let currentUser = null;
let mode = null;
let myColor = "white";
let opponentName = "Kompyuter";
let turn = "white";
let selected = null;
let currentGameId = null;

/* Timer state */
let myTime = 600;
let opponentTime = 600;
let timerInterval = null;
let timerRunning = false;"""

app = app.replace(old_timer_state, new_timer_state)

# Add timer element refs after chat element refs
old_refs = """const chatBox = document.getElementById("chatBox");
const chatInput = document.getElementById("chatInput");
const chatSendBtn = document.getElementById("chatSendBtn");
const chatMessages = document.getElementById("chatMessages");"""

new_refs = old_refs + """
const myTimerEl = document.getElementById("myTimer");
const oppTimerEl = document.getElementById("oppTimer");"""

app = app.replace(old_refs, new_refs)

# Update enterGame to init timers
old_enter = """function enterGame(){
  selected = null;
  showScreen("screen-game");
  if(chatBox) chatBox.classList.add("active");
  buildCoords();
  drawBoard();
  updateHeader();
}"""

new_enter = """function enterGame(){
  selected = null;
  myTime = 600;
  opponentTime = 600;
  showScreen("screen-game");
  if(chatBox) chatBox.classList.add("active");
  buildCoords();
  drawBoard();
  updateHeader();
  updateTimers();
  startTimer();
}

function startTimer(){
  stopTimer();
  timerRunning = true;
  timerInterval = setInterval(function(){
    if(turn === myColor){
      myTime = Math.max(0, myTime - 1);
      if(myTime === 0){ gameStatusEl.textContent = "Vaqt tugadi! " + opponentName + " yutdi!"; stopTimer(); }
    }else{
      opponentTime = Math.max(0, opponentTime - 1);
      if(opponentTime === 0){ gameStatusEl.textContent = "Vaqt tugadi! Siz yutdingiz!"; stopTimer(); }
    }
    updateTimers();
  }, 1000);
}

function stopTimer(){
  timerRunning = false;
  if(timerInterval) clearInterval(timerInterval);
  timerInterval = null;
}

function updateTimers(){
  if(myTimerEl) myTimerEl.textContent = formatTime(myTime);
  if(oppTimerEl) oppTimerEl.textContent = formatTime(opponentTime);
}

function formatTime(secs){
  var m = Math.floor(secs / 60);
  var s = secs % 60;
  return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
}"""

app = app.replace(old_enter, new_enter)

# Update leaveGame to stop timer
old_leave = """leaveGameBtn.addEventListener("click", () => {
  stopGamePoll();
  if(chatBox) chatBox.classList.remove("active");
  if(mode === "online" && currentGameId){ sendToServer({ type: "leaveGame", gameId: currentGameId }); }
  currentGameId = null;
  mode = null;
  enterLobby();
});"""

new_leave = """leaveGameBtn.addEventListener("click", () => {
  stopTimer();
  stopGamePoll();
  if(chatBox) chatBox.classList.remove("active");
  if(mode === "online" && currentGameId){ sendToServer({ type: "leaveGame", gameId: currentGameId }); }
  currentGameId = null;
  mode = null;
  enterLobby();
});"""

app = app.replace(old_leave, new_leave)

# Add timer to gameUpdate handler
old_update = """    case "gameUpdate":
      if(currentGameId === msg.gameId){
        pieces = msg.pieces;
        turn = msg.turn;
        drawBoard();
        updateHeader();
      }
      break;"""

new_update = """    case "gameUpdate":
      if(currentGameId === msg.gameId){
        pieces = msg.pieces;
        turn = msg.turn;
        drawBoard();
        updateHeader();
        updateTimers();
      }
      break;"""

app = app.replace(old_update, new_update)

# Also update the move handler to reset timer on move
old_move = """    pieces[to] = pieces[selected];
    delete pieces[selected];
    turn = myColor === "white" ? "black" : "white";
    selected = null;
    drawBoard();
    updateHeader();
    if(mode === "ai"){ setTimeout(aiMove, 350); }
    else{ sendToServer({ type: "move", gameId: currentGameId, pieces: pieces, turn: turn }); }"""

new_move = """    pieces[to] = pieces[selected];
    delete pieces[selected];
    turn = myColor === "white" ? "black" : "white";
    selected = null;
    drawBoard();
    updateHeader();
    updateTimers();
    if(mode === "ai"){ setTimeout(aiMove, 350); }
    else{ sendToServer({ type: "move", gameId: currentGameId, pieces: pieces, turn: turn }); }"""

app = app.replace(old_move, new_move)

with open(DST + "/app.js", "w", encoding="utf-8") as f:
    f.write(app)
print("app.js done:", len(app), "chars")


# ==================== 2. INDEX.HTML - add timer elements ====================
with open(SRC + "/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add timer to player tags
old_header = """  <div class="game-header">
    <div class="player-tag" id="playerTop"></div>
    <div class="game-status" id="gameStatus"></div>
    <div class="player-tag" id="playerBottom"></div>
  </div>"""

new_header = """  <div class="game-header">
    <div class="player-tag" id="playerTop">
      <span class="timer" id="oppTimer">10:00</span>
      <span class="pname" id="pTopName"></span>
      <span class="piece-icon" id="pTopIcon"></span>
    </div>
    <div class="game-status" id="gameStatus"></div>
    <div class="player-tag" id="playerBottom">
      <span class="piece-icon" id="pBotIcon"></span>
      <span class="pname" id="pBotName"></span>
      <span class="timer" id="myTimer">10:00</span>
    </div>
  </div>"""

html = html.replace(old_header, new_header)

with open(DST + "/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html done:", len(html), "chars")


# ==================== 3. STYLE.CSS - add timer + responsive styles ====================
with open(SRC + "/style.css", "r", encoding="utf-8") as f:
    css_old = f.read()

# Remove old chat styles (we'll re-add everything)
# Find where chat sidebar styles start and remove from there
cut_idx = css_old.find("/* ===== CHAT SIDEBAR ===== */")
if cut_idx != -1:
    css_old = css_old[:cut_idx]

css_new = css_old + """

/* ===== TIMER STYLES ===== */
.timer {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--gold);
  min-width: 48px;
  text-align: center;
  background: var(--panel-2);
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid var(--border);
}
.player-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--panel);
  border: 1px solid var(--border);
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  flex: 1;
  transition: .2s;
}
.player-tag .piece-icon { font-size: 18px; }
.player-tag .pname { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.player-tag.active-turn { border-color: var(--gold); box-shadow: 0 0 0 3px var(--gold-soft); color: var(--gold); }

/* ===== GAME LAYOUT ===== */
.game-layout {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.board-wrap { display: flex; gap: 6px; flex: 1; max-width: 100%; }
.board-col { flex: 1; min-width: 0; }

/* ===== CHAT SIDEBAR ===== */
.chat-sidebar {
  display: none;
  flex-direction: column;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  width: 220px;
  min-height: 300px;
  max-height: 420px;
  overflow: hidden;
  flex-shrink: 0;
}
.chat-sidebar.active { display: flex; }
.chat-header {
  font-size: 13px;
  font-weight: 600;
  color: var(--gold);
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: var(--panel-2);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.chat-msg {
  font-size: 13px;
  line-height: 1.4;
  padding: 4px 8px;
  border-radius: 6px;
  background: var(--panel-2);
  word-break: break-word;
}
.chat-msg b { color: var(--gold); font-weight: 600; }
.chat-input-row {
  display: flex;
  border-top: 1px solid var(--border);
  padding: 6px;
  gap: 4px;
}
.chat-input {
  flex: 1;
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 10px;
  color: var(--text);
  font-size: 12.5px;
  font-family: var(--font-body);
  outline: none;
}
.chat-input:focus { border-color: var(--gold); }
.chat-send {
  background: var(--gold);
  border: none;
  border-radius: 6px;
  color: #221a0c;
  font-size: 16px;
  padding: 6px 10px;
  cursor: pointer;
  transition: .15s;
  font-weight: 700;
}
.chat-send:hover { filter: brightness(1.1); }

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
  .game-layout { flex-direction: column; align-items: center; }
  .chat-sidebar { width: 100%; max-width: 460px; min-height: 180px; max-height: 260px; }
  .board { max-width: 460px; }
  .game-header { flex-wrap: wrap; justify-content: center; gap: 6px; }
  .player-tag { font-size: 12px; padding: 6px 10px; }
  .timer { font-size: 14px; min-width: 40px; }
  .cell { font-size: min(8vw, 32px); }
}

@media (max-width: 480px) {
  #screen-game { padding: 0 4px; }
  .game-header { gap: 4px; }
  .player-tag { padding: 4px 8px; font-size: 11px; }
  .timer { font-size: 12px; min-width: 36px; padding: 1px 5px; }
  .chat-sidebar { min-height: 140px; max-height: 200px; }
  .chat-messages { padding: 4px 6px; }
  .chat-msg { font-size: 12px; }
  .cell { font-size: min(10vw, 28px); }
  main { padding: 16px 8px 40px; }
  .topbar { padding: 12px 16px; }
  .brand { font-size: 17px; }
}
"""

with open(DST + "/style.css", "w", encoding="utf-8") as f:
    f.write(css_new)
print("style.css done:", len(css_new), "chars")

# ==================== 4. UPDATE updateHeader function to use new elements ====================
with open(DST + "/app.js", "r", encoding="utf-8") as f:
    app = f.read()

old_updateH = """function updateHeader(){
  const topName = myColor === "white" ? opponentName : currentUser;
  const bottomName = myColor === "white" ? currentUser : opponentName;
  const topColor = myColor === "white" ? "black" : "white";
  const bottomColor = myColor === "white" ? "white" : "black";
  playerTopEl.innerHTML = '<span class="piece">'+(topColor === "white" ? "♔" : "♚")+'</span> '+escapeHtml(topName);
  playerBottomEl.innerHTML = '<span class="piece">'+(bottomColor === "white" ? "♔" : "♚")+'</span> '+escapeHtml(bottomName);
  playerTopEl.classList.toggle("active-turn", turn === topColor);
  playerBottomEl.classList.toggle("active-turn", turn === bottomColor);
  if(mode === "ai"){
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Kompyuter o'ylanmoqda...";
  }else{
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Raqib navbati";
  }
}"""

new_updateH = """function updateHeader(){
  const topName = myColor === "white" ? opponentName : currentUser;
  const bottomName = myColor === "white" ? currentUser : opponentName;
  const topColor = myColor === "white" ? "black" : "white";
  const bottomColor = myColor === "white" ? "white" : "black";
  const topIcon = topColor === "white" ? "♔" : "♚";
  const botIcon = bottomColor === "white" ? "♔" : "♚";
  if(pTopName) pTopName.textContent = escapeHtml(topName);
  if(pBotName) pBotName.textContent = escapeHtml(bottomName);
  if(pTopIcon) pTopIcon.textContent = topIcon;
  if(pBotIcon) pBotIcon.textContent = botIcon;
  playerTopEl.classList.toggle("active-turn", turn === topColor);
  playerBottomEl.classList.toggle("active-turn", turn === bottomColor);
  if(mode === "ai"){
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Kompyuter o'ylanmoqda...";
  }else{
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Raqib navbati";
  }
}"""

app = app.replace(old_updateH, new_updateH)

# Add refs for new timer element IDs
old_ids = """const myTimerEl = document.getElementById("myTimer");
const oppTimerEl = document.getElementById("oppTimer");"""

new_ids = old_ids + """
const pTopName = document.getElementById("pTopName");
const pBotName = document.getElementById("pBotName");
const pTopIcon = document.getElementById("pTopIcon");
const pBotIcon = document.getElementById("pBotIcon");"""

app = app.replace(old_ids, new_ids)

with open(DST + "/app.js", "w", encoding="utf-8") as f:
    f.write(app)
print("app.js final:", len(app), "chars")

print("\n=== ALL DONE ===")
