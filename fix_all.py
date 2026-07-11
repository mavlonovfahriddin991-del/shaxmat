# Fix everything in one go
import sys, os

DST = "c:/Users/MARUFXON/Desktop/12"

# ==========================================================================
# 1. STYLE.CSS - complete rewrite for big board, big chat, responsive
# ==========================================================================
css = """:root{
  --bg: #10131a; --bg-2: #171b24; --panel: #1b212c; --panel-2: #232b38; --border: #2b3342;
  --ivory: #ece3d2; --walnut: #4a3728; --walnut-2: #5c4633; --gold: #c9a24b;
  --gold-soft: rgba(201,162,75,.16); --green: #4caf6d; --green-soft: rgba(76,175,109,.18);
  --red: #c1554a; --red-soft: rgba(193,85,74,.16); --text: #edeef2; --text-dim: #8b93a3;
  --font-display: 'Playfair Display', Georgia, serif; --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
*{ box-sizing:border-box; margin:0; padding:0; }
html,body{ height:100%; }
body{
  margin:0;
  background: radial-gradient(1200px 600px at 15% -10%, #1a2130 0%, transparent 60%),
    radial-gradient(1000px 500px at 100% 0%, #191d27 0%, transparent 55%), var(--bg);
  color:var(--text); font-family:var(--font-body); min-height:100%; display:flex; flex-direction:column;
}
::selection{ background:var(--gold-soft); }
.topbar{
  display:flex; align-items:center; justify-content:space-between; padding:16px 28px;
  border-bottom:1px solid var(--border); background:rgba(19,23,31,.6); backdrop-filter:blur(6px);
  position:sticky; top:0; z-index:10;
}
.brand{ font-family:var(--font-display); font-weight:700; font-size:20px; letter-spacing:.3px; display:flex; align-items:center; gap:10px; color:var(--ivory); }
.brand .glyph{ color:var(--gold); font-size:24px; }
.user-badge{ display:flex; align-items:center; gap:10px; background:var(--panel); border:1px solid var(--border); padding:6px 8px 6px 14px; border-radius:999px; font-size:14px; }
.user-badge .dot{ width:8px;height:8px;border-radius:50%; background:var(--green); box-shadow:0 0 0 0 rgba(76,175,109,.6); animation:pulse 2s infinite; }
.user-badge button{ border:none; background:var(--panel-2); color:var(--text-dim); padding:6px 12px; border-radius:999px; font-size:12.5px; font-family:var(--font-body); cursor:pointer; transition:.15s; }
.user-badge button:hover{ background:var(--red-soft); color:#f0a99f; }
@keyframes pulse{ 0%{ box-shadow:0 0 0 0 rgba(76,175,109,.55); } 70%{ box-shadow:0 0 0 8px rgba(76,175,109,0); } 100%{ box-shadow:0 0 0 0 rgba(76,175,109,0); } }
main{ flex:1; display:flex; align-items:flex-start; justify-content:center; padding:36px 20px 60px; }
.screen{ display:none; width:100%; max-width:960px; animation:fade .35s ease; }
.screen.active{ display:block; }
@keyframes fade{ from{ opacity:0; transform:translateY(6px);} to{ opacity:1; transform:translateY(0);} }
#screen-register{ max-width:440px; margin:0 auto; }
.reg-card{ background:var(--panel); border:1px solid var(--border); border-radius:18px; padding:40px 32px; text-align:center; box-shadow:0 20px 60px rgba(0,0,0,.35); }
.reg-card .king{ font-size:52px; color:var(--gold); margin-bottom:6px; filter:drop-shadow(0 6px 14px rgba(201,162,75,.25)); }
.reg-card h1{ font-family:var(--font-display); font-size:26px; margin:4px 0 6px; color:var(--ivory); }
.reg-card p{ color:var(--text-dim); font-size:14px; margin:0 0 26px; line-height:1.5; }
.reg-card input{ width:100%; padding:13px 16px; border-radius:10px; border:1px solid var(--border); background:var(--bg-2); color:var(--text); font-size:15px; font-family:var(--font-body); outline:none; margin-bottom:14px; transition:.15s; }
.reg-card input:focus{ border-color:var(--gold); box-shadow:0 0 0 3px var(--gold-soft); }
.btn-primary{ width:100%; padding:13px 16px; border-radius:10px; border:none; background:linear-gradient(180deg, var(--gold), #b8903f); color:#221a0c; font-weight:700; font-size:15px; font-family:var(--font-body); cursor:pointer; transition:.15s; }
.btn-primary:hover{ filter:brightness(1.08); transform:translateY(-1px); }
.btn-primary:disabled{ opacity:.5; cursor:not-allowed; transform:none; }
.reg-error{ color:#f0a99f; font-size:13px; margin-top:10px; min-height:16px; }
.invites-banner{ display:flex; flex-direction:column; gap:10px; margin-bottom:20px; }
.invite-card{ display:flex; align-items:center; justify-content:space-between; gap:14px; background:var(--gold-soft); border:1px solid rgba(201,162,75,.4); padding:14px 18px; border-radius:12px; animation:fade .3s ease; }
.invite-card .txt{ font-size:14.5px; }
.invite-card .txt b{ color:var(--gold); }
.invite-actions{ display:flex; gap:8px; }
.btn-small{ border:none; padding:8px 14px; border-radius:8px; font-size:13px; font-weight:600; font-family:var(--font-body); cursor:pointer; transition:.15s; }
.btn-accept{ background:var(--green); color:#0d2116; }
.btn-accept:hover{ filter:brightness(1.1); }
.btn-decline{ background:transparent; color:var(--text-dim); border:1px solid var(--border); }
.btn-decline:hover{ color:#f0a99f; border-color:var(--red); }
.lobby-grid{ display:grid; grid-template-columns:1.4fr 1fr; gap:20px; }
@media (max-width:720px){ .lobby-grid{ grid-template-columns:1fr; } }
.panel{ background:var(--panel); border:1px solid var(--border); border-radius:16px; padding:22px; }
.panel h2{ font-family:var(--font-display); font-size:18px; margin:0 0 4px; color:var(--ivory); }
.panel .sub{ color:var(--text-dim); font-size:13px; margin:0 0 18px; }
.online-list{ display:flex; flex-direction:column; gap:10px; min-height:60px; }
.player-row{ display:flex; align-items:center; justify-content:space-between; background:var(--panel-2); border:1px solid var(--border); padding:11px 14px; border-radius:11px; }
.player-row .who{ display:flex; align-items:center; gap:10px; font-size:14.5px; }
.player-row .dot{ width:8px; height:8px; border-radius:50%; background:var(--green); animation:pulse 2s infinite; }
.btn-invite{ background:transparent; border:1px solid var(--gold); color:var(--gold); padding:7px 13px; border-radius:8px; font-size:12.5px; font-weight:600; font-family:var(--font-body); cursor:pointer; transition:.15s; }
.btn-invite:hover{ background:var(--gold-soft); }
.btn-invite:disabled{ opacity:.4; cursor:default; }
.empty-state{ color:var(--text-dim); font-size:13.5px; padding:18px 4px; text-align:center; line-height:1.6; }
.ai-panel .glyph{ font-size:34px; color:var(--gold); margin-bottom:10px; display:block; }
.btn-ai{ width:100%; margin-top:6px; padding:12px; border-radius:10px; border:1px dashed var(--border); background:var(--panel-2); color:var(--text); font-weight:600; font-size:14px; font-family:var(--font-body); cursor:pointer; transition:.15s; }
.btn-ai:hover{ border-color:var(--gold); color:var(--gold); }
.ai-hint{ font-size:12.5px; color:var(--text-dim); margin-top:10px; line-height:1.5; }
#screen-waiting{ max-width:420px; margin:60px auto 0; text-align:center; }
#screen-waiting .spinner{ width:46px; height:46px; margin:0 auto 22px; border-radius:50%; border:3px solid var(--border); border-top-color:var(--gold); animation:spin 1s linear infinite; }
@keyframes spin{ to{ transform:rotate(360deg); } }
#screen-waiting p{ color:var(--text-dim); font-size:14px; line-height:1.6; }
#screen-waiting .target{ color:var(--gold); font-weight:600; }

/* ================================================================
   GAME - BIG BOARD + BIG CHAT
   ================================================================ */
#screen-game{ max-width:1000px; margin:0 auto; }

.game-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:16px;
  gap:12px;
}
.player-tag{
  display:flex;
  align-items:center;
  gap:10px;
  background:var(--panel);
  border:1px solid var(--border);
  padding:10px 16px;
  border-radius:12px;
  font-size:15px;
  font-weight:600;
  flex:1;
  transition:.2s;
}
.player-tag.active-turn{ border-color:var(--gold); box-shadow:0 0 0 3px var(--gold-soft); color:var(--gold); }
.player-tag .piece-icon{ font-size:22px; }
.player-tag .pname{ flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.game-status{
  font-family:var(--font-mono);
  font-size:13px;
  color:var(--text-dim);
  text-align:center;
  margin:0 10px;
  white-space:nowrap;
  font-weight:500;
}

/* Timer */
.timer{
  font-family:'JetBrains Mono',monospace;
  font-size:20px;
  font-weight:700;
  color:var(--gold);
  min-width:60px;
  text-align:center;
  background:var(--panel-2);
  padding:4px 12px;
  border-radius:8px;
  border:1px solid var(--border);
}

/* Game layout - side by side */
.game-layout{
  display:flex;
  gap:20px;
  align-items:flex-start;
}

/* Board wrap */
.board-wrap{
  display:flex;
  gap:8px;
  flex:0 0 auto;
  width:540px;
  max-width:100%;
}
.ranks{
  display:flex;
  flex-direction:column;
  justify-content:space-around;
  padding:4px 0;
}
.ranks span, .files span{ color:var(--text-dim); font-family:var(--font-mono); font-size:12px; font-weight:500; }
.files{
  display:flex;
  justify-content:space-around;
  padding-left:4px;
  margin-top:6px;
}
.board-col{ flex:1; min-width:0; }

/* Board - fixed aspect ratio square */
.board{
  display:grid;
  grid-template-columns:repeat(8,1fr);
  grid-template-rows:repeat(8,1fr);
  width:100%;
  aspect-ratio:1/1;
  border-radius:12px;
  overflow:hidden;
  border:3px solid var(--walnut-2);
  box-shadow:0 20px 50px rgba(0,0,0,.45);
}

/* Cells - use aspect-ratio to keep squares */
.cell{
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  user-select:none;
  position:relative;
  transition:background .1s;
  /* Don't set font-size to vw, use a fixed large size that fits */
  font-size:clamp(24px, 5.5vw, 44px);
}
.cell.white{ background:var(--ivory); }
.cell.black{ background:var(--walnut); }
.cell.selected{ box-shadow:inset 0 0 0 3px var(--gold); }
.cell.wpiece{
  color:#c1863f;
  -webkit-text-stroke:1.5px #4a3016;
  text-shadow:0 2px 3px rgba(0,0,0,.4);
}
.cell.bpiece{
  color:#151008;
  -webkit-text-stroke:1.5px #000;
  text-shadow:0 1px 2px rgba(0,0,0,.5);
}
.cell.hint::after{
  content:'';
  position:absolute;
  width:28%;
  height:28%;
  border-radius:50%;
  pointer-events:none;
}
.cell.white.hint::after{ background:rgba(30,20,10,.35); }
.cell.black.hint::after{ background:rgba(255,255,255,.45); }
.cell.hint-capture::after{
  content:'';
  position:absolute;
  inset:6%;
  border-radius:50%;
  border:3px solid;
  background:transparent;
  pointer-events:none;
}
.cell.white.hint-capture::after{ border-color:rgba(30,20,10,.45); }
.cell.black.hint-capture::after{ border-color:rgba(255,255,255,.5); }

/* ===== CHAT SIDEBAR - BIG ===== */
.chat-sidebar{
  display:none;
  flex-direction:column;
  background:var(--panel);
  border:1px solid var(--border);
  border-radius:14px;
  width:300px;
  min-height:400px;
  max-height:540px;
  overflow:hidden;
  flex-shrink:0;
}
.chat-sidebar.active{ display:flex; }
.chat-header{
  font-size:15px;
  font-weight:600;
  color:var(--gold);
  padding:12px 16px;
  border-bottom:1px solid var(--border);
  background:var(--panel-2);
}
.chat-messages{
  flex:1;
  overflow-y:auto;
  padding:10px 12px;
  display:flex;
  flex-direction:column;
  gap:6px;
}
.chat-msg{
  font-size:14px;
  line-height:1.5;
  padding:6px 10px;
  border-radius:8px;
  background:var(--panel-2);
  word-break:break-word;
}
.chat-msg b{ color:var(--gold); font-weight:600; }
.chat-input-row{
  display:flex;
  border-top:1px solid var(--border);
  padding:8px;
  gap:6px;
}
.chat-input{
  flex:1;
  background:var(--bg-2);
  border:1px solid var(--border);
  border-radius:8px;
  padding:9px 12px;
  color:var(--text);
  font-size:14px;
  font-family:var(--font-body);
  outline:none;
}
.chat-input:focus{ border-color:var(--gold); }
.chat-send{
  background:var(--gold);
  border:none;
  border-radius:8px;
  color:#221a0c;
  font-size:18px;
  padding:8px 14px;
  cursor:pointer;
  transition:.15s;
  font-weight:700;
}
.chat-send:hover{ filter:brightness(1.1); }

.game-actions{ display:flex; justify-content:center; margin-top:20px; }
.btn-leave{ border:1px solid var(--border); background:var(--panel); color:var(--text-dim); padding:10px 24px; border-radius:10px; font-size:14px; font-family:var(--font-body); cursor:pointer; transition:.15s; }
.btn-leave:hover{ color:#f0a99f; border-color:var(--red); }
.note{ text-align:center; color:var(--text-dim); font-size:12px; margin-top:24px; line-height:1.6; }

/* ===== RESPONSIVE ===== */
@media (max-width:960px){
  .game-layout{ flex-direction:column; align-items:center; }
  .chat-sidebar{ width:100%; max-width:540px; min-height:200px; max-height:300px; }
  .board-wrap{ width:100%; max-width:540px; }
  .cell{ font-size:clamp(22px, 6vw, 40px); }
}
@media (max-width:600px){
  .board-wrap{ width:100%; max-width:100%; }
  .cell{ font-size:clamp(18px, 8vw, 34px); }
  .player-tag{ padding:6px 10px; font-size:13px; }
  .timer{ font-size:16px; min-width:48px; padding:2px 8px; }
  .chat-sidebar{ min-height:160px; max-height:240px; }
  main{ padding:16px 8px 40px; }
  .topbar{ padding:12px 16px; }
  .brand{ font-size:17px; }
  .game-header{ gap:6px; }
}
@media (max-width:400px){
  .cell{ font-size:clamp(14px, 9vw, 26px); }
  .timer{ font-size:14px; min-width:40px; }
}
"""

with open(DST + "/style.css", "w", encoding="utf-8") as f:
    f.write(css)
print("style.css rewritten:", len(css), "chars")

# ==========================================================================
# 2. INDEX.HTML - ensure no extra quotes issue
# ==========================================================================
html = '<!DOCTYPE html>\n'
html += '<html lang="uz">\n'
html += '<head>\n'
html += '<meta charset="UTF-8">\n'
html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
html += '<title>Shaxmat Arena</title>\n'
html += '<link rel="stylesheet" href="style.css">\n'
html += '</head>\n'
html += '<body>\n'
html += '<header class="topbar">\n'
html += '  <div class="brand"><span class="glyph">&#9822;</span> Shaxmat Arena</div>\n'
html += '  <div class="user-badge" id="userBadge" style="display:none">\n'
html += '    <span class="dot"></span> <span id="userBadgeName"></span>\n'
html += '    <button id="logoutBtn">Chiqish</button>\n'
html += '  </div>\n'
html += '</header>\n'
html += '<main>\n'
html += '<section id="screen-register" class="screen active">\n'
html += '  <div class="reg-card">\n'
html += '    <div class="king">&#9818;</div>\n'
html += '    <h1>Ro\'yxatdan o\'tish</h1>\n'
html += '    <p>Ismingizni kiriting va onlayn o\'yinchilar bilan shaxmat o\'ynang.</p>\n'
html += '    <input id="usernameInput" type="text" placeholder="Foydalanuvchi nomi" maxlength="18" autocomplete="off">\n'
html += '    <button class="btn-primary" id="registerBtn">O\'yinga kirish</button>\n'
html += '    <div class="reg-error" id="regError"></div>\n'
html += '  </div>\n'
html += '</section>\n'
html += '<section id="screen-lobby" class="screen">\n'
html += '  <div class="invites-banner" id="incomingInvites"></div>\n'
html += '  <div class="lobby-grid">\n'
html += '    <div class="panel players-panel">\n'
html += '      <h2>Onlayn o\'yinchilar</h2>\n'
html += '      <p class="sub">Taklif yuboring va real vaqtda o\'ynang</p>\n'
html += '      <div class="online-list" id="onlineList"><div class="empty-state">Qidirilmoqda...</div></div>\n'
html += '    </div>\n'
html += '    <div class="panel ai-panel">\n'
html += '      <span class="glyph">&#9823;</span>\n'
html += '      <h2>Kompyuterga qarshi</h2>\n'
html += '      <p class="sub">Onlayn raqib bo\'lmasa, sun\'iy intellektga qarshi mashq qiling</p>\n'
html += '      <button class="btn-ai" id="playAiBtn">Sun\'iy intellekt bilan o\'ynash</button>\n'
html += '      <div class="ai-hint" id="aiHint"></div>\n'
html += '    </div>\n'
html += '  </div>\n'
html += '</section>\n'
html += '<section id="screen-waiting" class="screen">\n'
html += '  <div class="spinner"></div>\n'
html += '  <p><span class="target" id="waitingTarget"></span> javobini kutmoqdamiz...</p>\n'
html += '  <div class="game-actions" style="margin-top:24px"><button class="btn-leave" id="cancelWaitBtn">Bekor qilish</button></div>\n'
html += '</section>\n'
html += '<section id="screen-game" class="screen">\n'
html += '  <div class="game-header">\n'
html += '    <div class="player-tag" id="playerTop">\n'
html += '      <span class="timer" id="oppTimer">10:00</span>\n'
html += '      <span class="pname" id="pTopName"></span>\n'
html += '      <span class="piece-icon" id="pTopIcon"></span>\n'
html += '    </div>\n'
html += '    <div class="game-status" id="gameStatus"></div>\n'
html += '    <div class="player-tag" id="playerBottom">\n'
html += '      <span class="piece-icon" id="pBotIcon"></span>\n'
html += '      <span class="pname" id="pBotName"></span>\n'
html += '      <span class="timer" id="myTimer">10:00</span>\n'
html += '    </div>\n'
html += '  </div>\n'
html += '  <div class="game-layout">\n'
html += '    <div class="board-wrap">\n'
html += '      <div class="ranks" id="ranksCol"></div>\n'
html += '      <div class="board-col">\n'
html += '        <div class="board" id="board"></div>\n'
html += '        <div class="files" id="filesRow"></div>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '    <div class="chat-sidebar" id="chatBox">\n'
html += '      <div class="chat-header">&#128172; Chat</div>\n'
html += '      <div class="chat-messages" id="chatMessages"></div>\n'
html += '      <div class="chat-input-row">\n'
html += '        <input class="chat-input" id="chatInput" type="text" placeholder="Xabar yozing..." autocomplete="off">\n'
html += '        <button class="chat-send" id="chatSendBtn">&#10148;</button>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '  </div>\n'
html += '  <div class="game-actions"><button class="btn-leave" id="leaveGameBtn">O\'yindan chiqish</button></div>\n'
html += '</section>\n'
html += '<p class="note">Online o\'yin WebSocket orqali sinxronlanadi. Har bir o\'yinchiga 10 daqiqa vaqt.</p>\n'
html += '</main>\n'
html += '<script src="app.js"></script>\n'
html += '</body>\n'
html += '</html>'

with open(DST + "/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html rewritten:", len(html), "chars")

print("\n=== DONE FIXING ===")
