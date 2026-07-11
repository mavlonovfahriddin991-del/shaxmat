(function(){
"use strict";

const WHITE_SYM = new Set(["♙","♖","♘","♗","♕","♔"]);

function initialPieces(){
  return {
    0:"♜",1:"♞",2:"♝",3:"♛",4:"♚",5:"♝",6:"♞",7:"♜",
    8:"♟",9:"♟",10:"♟",11:"♟",12:"♟",13:"♟",14:"♟",15:"♟",
    48:"♙",49:"♙",50:"♙",51:"♙",52:"♙",53:"♙",54:"♙",55:"♙",
    56:"♖",57:"♘",58:"♗",59:"♕",60:"♔",61:"♗",62:"♘",63:"♖"
  };
}

function pieceColor(p){ return WHITE_SYM.has(p) ? "white" : "black"; }

function pieceType(p){
  switch(p){
    case "♙": case "♟": return "pawn";
    case "♖": case "♜": return "rook";
    case "♘": case "♞": return "knight";
    case "♗": case "♝": return "bishop";
    case "♕": case "♛": return "queen";
    case "♔": case "♚": return "king";
    default: return null;
  }
}

let pieces = {};

function path(f,t){
  let fx=Math.floor(f/8), fy=f%8;
  let tx=Math.floor(t/8), ty=t%8;
  let dx=Math.sign(tx-fx);
  let dy=Math.sign(ty-fy);
  let x=fx+dx, y=fy+dy;
  while(x!==tx || y!==ty){
    if(pieces[x*8+y]) return false;
    x+=dx; y+=dy;
  }
  return true;
}

function valid(f,t){
  if(f===t) return false;
  let p = pieces[f];
  if(!p) return false;
  let c = pieceColor(p);
  let target = pieces[t];
  if(target && pieceColor(target)===c) return false;

  let fx=Math.floor(f/8), fy=f%8;
  let tx=Math.floor(t/8), ty=t%8;
  let dx=tx-fx, dy=ty-fy;
  let type = pieceType(p);

  if(type==="pawn"){
    let dir = c==="white" ? -1 : 1;
    let startRow = c==="white" ? 6 : 1;
    if(dy===0 && dx===dir && !target) return true;
    if(dy===0 && dx===2*dir && fx===startRow && !target && !pieces[f+8*dir]) return true;
    if(Math.abs(dy)===1 && dx===dir && target) return true;
    return false;
  }
  if(type==="rook"){
    if(dx!==0 && dy!==0) return false;
    return path(f,t);
  }
  if(type==="bishop"){
    
    if(Math.abs(dx)!==Math.abs(dy)) return false;
    return path(f,t);
  }
  if(type==="queen"){
    if(dx===0 || dy===0 || Math.abs(dx)===Math.abs(dy)) return path(f,t);
    return false;
  }
  if(type==="knight"){
    return (Math.abs(dx)===2 && Math.abs(dy)===1) || (Math.abs(dx)===1 && Math.abs(dy)===2);
  }
  if(type==="king"){
    return Math.abs(dx)<=1 && Math.abs(dy)<=1;
  }
  return false;
}

let currentUser = null;
let mode = null;
let myColor = "white";
let opponentName = "Kompyuter";
let turn = "white";
let selected = null;
let currentGameId = null;

/* Timer */
let myTime = 600;
let opponentTime = 600;
let timerInterval = null;

let ws = null;
let heartbeatTimer = null;
let gameTimer = null;
let lobbyTimer = null;

function clearTimer(t){ if(t) clearInterval(t); return null; }

function showScreen(id){
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

function connectWebSocket(){
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  ws = new WebSocket(proto + "//" + host + window.location.pathname);

  ws.onopen = () => { console.log("WebSocket ulandi"); };

  ws.onmessage = (event) => {
    let msg;
    try { msg = JSON.parse(event.data); } catch { return; }
    handleServerMessage(msg);
  };

  ws.onclose = () => {
    console.log("WebSocket uzildi, 3 soniyadan keyin qayta ulanadi...");
    setTimeout(connectWebSocket, 3000);
  };

  ws.onerror = (err) => { console.error("WebSocket xatosi:", err); };
}

function sendToServer(data){
  if(ws && ws.readyState === WebSocket.OPEN){
    ws.send(JSON.stringify(data));
  }
}

function handleServerMessage(msg){
  switch(msg.type){
    case "error":
      alert(msg.text);
      registerBtn.disabled = false;
      break;
    case "registered":
      currentUser = msg.username;
      userBadge.style.display = "flex";
      userBadgeName.textContent = currentUser;
      registerBtn.disabled = false;
      startHeartbeat();
      enterLobby();
      break;
    case "users":
      refreshOnlineListUI(msg.list);
      break;
    case "invite":
      showInviteNotification(msg.from, msg.gameId);
      break;
    case "inviteSent":
      currentGameId = msg.gameId;
      waitingTarget.textContent = msg.target;
      stopLobbyTimers();
      showScreen("screen-waiting");
      break;
    case "inviteDeclined":
      currentGameId = null;
      enterLobby();
      break;
    case "gameStart":
      stopLobbyTimers();
      mode = "online";
      myColor = msg.yourColor;
      opponentName = myColor === "white" ? msg.black : msg.white;
      pieces = msg.pieces;
      turn = msg.turn;
      currentGameId = msg.gameId;
      enterGame();
      break;
    case "gameUpdate":
      if(currentGameId === msg.gameId){
        pieces = msg.pieces;
        turn = msg.turn;
        drawBoard();
        updateHeader();
        updateTimers();
      }
      break;
        case "chat":
      if(currentGameId === msg.gameId){
        addChatMessage(msg.from, msg.text);
      }
      break;
        case "gameEnded":
      if(currentGameId === msg.gameId){
        alert("Raqib o'yindan chiqib ketdi.");
        currentGameId = null;
        mode = null;
        enterLobby();
      }
      break;
  }
}

const usernameInput = document.getElementById("usernameInput");
const registerBtn = document.getElementById("registerBtn");
const regError = document.getElementById("regError");
const userBadge = document.getElementById("userBadge");
const userBadgeName = document.getElementById("userBadgeName");
const logoutBtn = document.getElementById("logoutBtn");

function register(){
  const name = usernameInput.value.trim();
  if(!name){ regError.textContent = "Iltimos, ism kiriting."; return; }
  if(name.length < 2){ regError.textContent = "Ism kamida 2 ta belgidan iborat bo'lsin."; return; }
  registerBtn.disabled = true;
  regError.textContent = "";
  sendToServer({ type: "register", username: name });
}

function startHeartbeat(){
  heartbeatTimer = clearTimer(heartbeatTimer);
  heartbeatTimer = setInterval(() => { sendToServer({ type: "heartbeat" }); }, 5000);
}

function logout(){
  stopLobbyTimers();
  stopGamePoll();
  heartbeatTimer = clearTimer(heartbeatTimer);
  if(ws) ws.close();
  currentUser = null;
  currentGameId = null;
  mode = null;
  userBadge.style.display = "none";
  usernameInput.value = "";
  showScreen("screen-register");
}

registerBtn.addEventListener("click", register);
usernameInput.addEventListener("keydown", e => { if(e.key === "Enter") register(); });
logoutBtn.addEventListener("click", logout);

const onlineListEl = document.getElementById("onlineList");
const incomingInvitesEl = document.getElementById("incomingInvites");
const playAiBtn = document.getElementById("playAiBtn");
const aiHint = document.getElementById("aiHint");

let pendingInvites = [];

function enterLobby(){
  showScreen("screen-lobby");
  refreshInvitesUI();
}

function stopLobbyTimers(){ lobbyTimer = clearTimer(lobbyTimer); }

function refreshOnlineListUI(list){
  const filtered = list.filter(u => u !== currentUser);
  if(filtered.length === 0){
    onlineListEl.innerHTML = '<div class="empty-state">Hozircha boshqa onlayn o\'yinchilar yo\'q.<br>Do\'stingizni chaqiring yoki sun\'iy intellektga qarshi o\'ynang.</div>';
    playAiBtn.disabled = false;
    aiHint.textContent = "Hozir onlayn raqib yo'q — kompyuterga qarshi o'ynashingiz mumkin.";
  }else{
    onlineListEl.innerHTML = "";
    filtered.sort().forEach(u => {
      const row = document.createElement("div");
      row.className = "player-row";
      row.innerHTML = '<div class="who"><span class="dot"></span>'+escapeHtml(u)+'</div><button class="btn-invite">Taklif qilish</button>';
      row.querySelector(".btn-invite").addEventListener("click", () => sendInvite(u));
      onlineListEl.appendChild(row);
    });
    playAiBtn.disabled = true;
    aiHint.textContent = "Onlayn o'yinchilar mavjud bo'lganda, avval ular bilan o'ynang.";
  }
}

function refreshInvitesUI(){
  if(pendingInvites.length === 0){ incomingInvitesEl.innerHTML = ""; return; }
  incomingInvitesEl.innerHTML = "";
  pendingInvites.forEach(inv => {
    const card = document.createElement("div");
    card.className = "invite-card";
    card.innerHTML = '<div class="txt"><b>'+escapeHtml(inv.from)+'</b> sizni o\'yinga taklif qilmoqda</div><div class="invite-actions"><button class="btn-small btn-accept">Qabul qilish</button><button class="btn-small btn-decline">Rad etish</button></div>';
    card.querySelector(".btn-accept").addEventListener("click", () => acceptInvite(inv));
    card.querySelector(".btn-decline").addEventListener("click", () => declineInvite(inv));
    incomingInvitesEl.appendChild(card);
  });
}

function showInviteNotification(from, gameId){
  pendingInvites.push({ from, gameId });
  refreshInvitesUI();
}

function escapeHtml(s){ const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }

const waitingTarget = document.getElementById("waitingTarget");
const cancelWaitBtn = document.getElementById("cancelWaitBtn");

function sendInvite(target){ sendToServer({ type: "sendInvite", target }); }

cancelWaitBtn.addEventListener("click", () => {
  if(currentGameId){ sendToServer({ type: "declineInvite", gameId: currentGameId }); }
  currentGameId = null;
  enterLobby();
});

function acceptInvite(inv){
  pendingInvites = pendingInvites.filter(i => i.gameId !== inv.gameId);
  refreshInvitesUI();
  sendToServer({ type: "acceptInvite", gameId: inv.gameId });
}

function declineInvite(inv){
  pendingInvites = pendingInvites.filter(i => i.gameId !== inv.gameId);
  refreshInvitesUI();
  sendToServer({ type: "declineInvite", gameId: inv.gameId });
}

playAiBtn.addEventListener("click", () => {
  if(playAiBtn.disabled) return;
  mode = "ai";
  myColor = "white";
  opponentName = "Kompyuter";
  pieces = initialPieces();
  turn = "white";
  currentGameId = null;
  enterGame();
});

const boardEl = document.getElementById("board");
const playerTopEl = document.getElementById("playerTop");
const playerBottomEl = document.getElementById("playerBottom");
const gameStatusEl = document.getElementById("gameStatus");
const leaveGameBtn = document.getElementById("leaveGameBtn");
const ranksCol = document.getElementById("ranksCol");
const filesRow = document.getElementById("filesRow");
const chatBox = document.getElementById("chatBox");
const chatInput = document.getElementById("chatInput");
const chatSendBtn = document.getElementById("chatSendBtn");
const chatMessages = document.getElementById("chatMessages");
const myTimerEl = document.getElementById("myTimer");
const oppTimerEl = document.getElementById("oppTimer");
const pTopName = document.getElementById("pTopName");
const pBotName = document.getElementById("pBotName");
const pTopIcon = document.getElementById("pTopIcon");
const pBotIcon = document.getElementById("pBotIcon");

function enterGame(){
  selected = null;
  showScreen("screen-game");
  myTime = 600;
  opponentTime = 600;
  updateTimers();
  startTimer();
  if(chatBox) chatBox.classList.add("active");
  buildCoords();
  drawBoard();
  updateHeader();
}

function startTimer(){
  if(timerInterval) clearInterval(timerInterval);
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
}

function buildCoords(){
  ranksCol.innerHTML = "";
  for(let i=8;i>=1;i--){ const s=document.createElement("span"); s.textContent=i; ranksCol.appendChild(s); }
  filesRow.innerHTML = "";
  ["a","b","c","d","e","f","g","h"].forEach(f => { const s=document.createElement("span"); s.textContent=f; filesRow.appendChild(s); });
}

function updateHeader(){
  const topName = myColor === "white" ? opponentName : currentUser;
  const bottomName = myColor === "white" ? currentUser : opponentName;
  const topColor = myColor === "white" ? "black" : "white";
  const bottomColor = myColor === "white" ? "white" : "black";
  if(pTopName) pTopName.textContent = escapeHtml(topName);
  if(pBotName) pBotName.textContent = escapeHtml(bottomName);
  if(pTopIcon) pTopIcon.textContent = topColor === "white" ? "♔" : "♚";
  if(pBotIcon) pBotIcon.textContent = bottomColor === "white" ? "♔" : "♚";
  playerTopEl.classList.toggle("active-turn", turn === topColor);
  playerBottomEl.classList.toggle("active-turn", turn === bottomColor);
  if(mode === "ai"){
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Kompyuter o'ylanmoqda...";
  }else{
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Raqib navbati";
  }
}

function drawBoard(){
  boardEl.innerHTML = "";
  for(let i=0;i<64;i++){
    const cell = document.createElement("div");
    const r = Math.floor(i/8), c = i%8;
    cell.className = "cell " + ((r+c)%2 ? "black" : "white");
    if(pieces[i]){
      cell.textContent = pieces[i];
      cell.classList.add(pieceColor(pieces[i]) === "white" ? "wpiece" : "bpiece");
      cell.draggable = true;
      cell.addEventListener("dragstart", () => { selected = i; });
      cell.addEventListener("click", () => onCellClick(i));
    }else{
      cell.addEventListener("click", () => onCellClick(i));
    }
    if(selected === i) cell.classList.add("selected");
    if(selected !== null && selected !== i && turn === myColor && valid(selected, i)){
      cell.classList.add(pieces[i] ? "hint-capture" : "hint");
    }
    cell.addEventListener("dragover", e => e.preventDefault());
    cell.addEventListener("drop", () => attemptMove(i));
    boardEl.appendChild(cell);
  }
}

function onCellClick(i){
  if(selected === null){ if(pieces[i]) { selected = i; drawBoard(); } }
  else if(selected === i){ selected = null; drawBoard(); }
  else{ attemptMove(i); }
}

function attemptMove(to){
  if(selected === null) return;
  if(turn !== myColor){ selected = null; drawBoard(); return; }
  if(valid(selected, to)){
    pieces[to] = pieces[selected];
    delete pieces[selected];
    turn = myColor === "white" ? "black" : "white";
    selected = null;
    drawBoard();
    updateHeader();
    updateTimers();
    if(mode === "ai"){ setTimeout(aiMove, 350); }
    else{ sendToServer({ type: "move", gameId: currentGameId, pieces: pieces, turn: turn }); }
  }else{ selected = null; drawBoard(); }
}

function aiMove(){
  const moves = [];
  for(const f in pieces){
    const fi = Number(f);
    if(pieceColor(pieces[fi]) !== "black") continue;
    for(let t=0;t<64;t++){ if(valid(fi, t)) moves.push([fi, t]); }
  }
  if(moves.length === 0){ gameStatusEl.textContent = "O'yin tugadi"; return; }
  const capture = moves.filter(m => pieces[m[1]]);
  const best = capture.length ? capture[Math.floor(Math.random()*capture.length)] : moves[Math.floor(Math.random()*moves.length)];
  pieces[best[1]] = pieces[best[0]];
  delete pieces[best[0]];
  turn = "white";
  drawBoard();
  updateHeader();
}

function addChatMessage(who, txt){
  var el = document.createElement("div");
  el.className = "chat-msg";
  el.innerHTML = "<b>" + escapeHtml(who) + ":</b> " + escapeHtml(txt);
  chatMessages.appendChild(el);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendChat(){
  var txt = chatInput.value.trim();
  if(!txt || !currentGameId || mode !== "online") return;
  sendToServer({ type: "chatMsg", gameId: currentGameId, text: txt });
  chatInput.value = "";
}

function stopGamePoll(){ gameTimer = clearTimer(gameTimer); }

chatSendBtn.addEventListener("click", sendChat);
chatInput.addEventListener("keydown", function(e){ if(e.key === "Enter") sendChat(); });

leaveGameBtn.addEventListener("click", () => {
  stopTimer();
  stopGamePoll();
  if(chatBox) chatBox.classList.remove("active");
  if(mode === "online" && currentGameId){ sendToServer({ type: "leaveGame", gameId: currentGameId }); }
  currentGameId = null;
  mode = null;
  enterLobby();
});

connectWebSocket();

})();

