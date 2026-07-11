
import sys, os

base = "c:/Users/MARUFXON/Desktop/12"
os.chdir(base)

# ===== INDEX.HTML =====
html = '''<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaxmat Arena</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="glyph">&#9822;</span> Shaxmat Arena</div>
  <div class="user-badge" id="userBadge" style="display:none">
    <span class="dot"></span> <span id="userBadgeName"></span>
    <button id="logoutBtn">Chiqish</button>
  </div>
</header>
<main>
<section id="screen-register" class="screen active">
  <div class="reg-card">
    <div class="king">&#9818;</div>
    <h1>Ro'yxatdan o'tish</h1>
    <p>Ismingizni kiriting va onlayn o'yinchilar bilan shaxmat o'ynang.</p>
    <input id="usernameInput" type="text" placeholder="Foydalanuvchi nomi" maxlength="18" autocomplete="off">
    <button class="btn-primary" id="registerBtn">O'yinga kirish</button>
    <div class="reg-error" id="regError"></div>
  </div>
</section>
<section id="screen-lobby" class="screen">
  <div class="invites-banner" id="incomingInvites"></div>
  <div class="lobby-grid">
    <div class="panel players-panel">
      <h2>Onlayn o'yinchilar</h2>
      <p class="sub">Taklif yuboring va real vaqtda o'ynang</p>
      <div class="online-list" id="onlineList"><div class="empty-state">Qidirilmoqda...</div></div>
    </div>
    <div class="panel ai-panel">
      <span class="glyph">&#9823;</span>
      <h2>Kompyuterga qarshi</h2>
      <p class="sub">Onlayn raqib bo'lmasa, sun'iy intellektga qarshi mashq qiling</p>
      <button class="btn-ai" id="playAiBtn">Sun'iy intellekt bilan o'ynash</button>
      <div class="ai-hint" id="aiHint"></div>
    </div>
  </div>
</section>
<section id="screen-waiting" class="screen">
  <div class="spinner"></div>
  <p><span class="target" id="waitingTarget"></span> javobini kutmoqdamiz...</p>
  <div class="game-actions" style="margin-top:24px"><button class="btn-leave" id="cancelWaitBtn">Bekor qilish</button></div>
</section>
<section id="screen-game" class="screen">
  <div class="game-header">
    <div class="player-tag" id="playerTop"></div>
    <div class="game-status" id="gameStatus"></div>
    <div class="player-tag" id="playerBottom"></div>
  </div>
  <div class="game-layout">
    <div class="board-wrap">
      <div class="ranks" id="ranksCol"></div>
      <div class="board-col">
        <div class="board" id="board"></div>
        <div class="files" id="filesRow"></div>
      </div>
    </div>
    <div class="chat-sidebar" id="chatBox">
      <div class="chat-header">&#128172; Chat</div>
      <div class="chat-messages" id="chatMessages"></div>
      <div class="chat-input-row">
        <input class="chat-input" id="chatInput" type="text" placeholder="Xabar yozing..." autocomplete="off">
        <button class="chat-send" id="chatSendBtn">&#10148;</button>
      </div>
    </div>
  </div>
  <div class="game-actions"><button class="btn-leave" id="leaveGameBtn">O'yindan chiqish</button></div>
</section>
<p class="note">Onlayn o'yinchilar WebSocket orqali real vaqtda sinxronlanadi.</p>
</main>
<script src="app.js"></script>
</body>
</html>'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html done:", len(html), "chars")

# ===== UPDATE STYLE.CSS =====
css_add = '''

/* ===== CHAT SIDEBAR ===== */
.game-layout {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
@media (max-width: 820px) {
  .game-layout { flex-direction: column; align-items: center; }
}
.chat-sidebar {
  display: none;
  flex-direction: column;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  width: 220px;
  min-height: 340px;
  max-height: 440px;
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
'''

with open("style.css", "a", encoding="utf-8") as f:
    f.write(css_add)
print("style.css updated")
