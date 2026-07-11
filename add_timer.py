# Add timer support back to app.js
d = open("c:/Users/MARUFXON/Desktop/12/app.js", "r", encoding="utf-8").read()

# 1. Timer variables after currentGameId
old = 'let currentGameId = null;\n\nlet ws = null;'
new = 'let currentGameId = null;\n\n/* Timer */\nlet myTime = 600;\nlet opponentTime = 600;\nlet timerInterval = null;\n\nlet ws = null;'
d = d.replace(old, new)

# 2. Timer element refs after chatMessages
old = 'const chatMessages = document.getElementById("chatMessages");'
new = old + '\nconst myTimerEl = document.getElementById("myTimer");\nconst oppTimerEl = document.getElementById("oppTimer");\nconst pTopName = document.getElementById("pTopName");\nconst pBotName = document.getElementById("pBotName");\nconst pTopIcon = document.getElementById("pTopIcon");\nconst pBotIcon = document.getElementById("pBotIcon");'
d = d.replace(old, new)

# 3. Update enterGame
old = 'function enterGame(){\n  selected = null;\n  showScreen("screen-game");\n  if(chatBox) chatBox.classList.add("active");\n  buildCoords();\n  drawBoard();\n  updateHeader();\n}'
new = 'function enterGame(){\n  selected = null;\n  showScreen("screen-game");\n  myTime = 600;\n  opponentTime = 600;\n  updateTimers();\n  startTimer();\n  if(chatBox) chatBox.classList.add("active");\n  buildCoords();\n  drawBoard();\n  updateHeader();\n}'
d = d.replace(old, new)

# 4. Timer functions before buildCoords
old = 'function buildCoords(){'
new = '''function startTimer(){
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

function buildCoords(){'''
d = d.replace(old, new)

# 5. Update updateHeader - use new IDs
old = '''function updateHeader(){
  const topName = myColor === "white" ? opponentName : currentUser;
  const bottomName = myColor === "white" ? currentUser : opponentName;
  const topColor = myColor === "white" ? "black" : "white";
  const bottomColor = myColor === "white" ? "white" : "black";
  playerTopEl.innerHTML = '<span class="piece">'+(topColor === "white" ? "\u2654" : "\u265a")+'</span> '+escapeHtml(topName);
  playerBottomEl.innerHTML = '<span class="piece">'+(bottomColor === "white" ? "\u2654" : "\u265a")+'</span> '+escapeHtml(bottomName);
  playerTopEl.classList.toggle("active-turn", turn === topColor);
  playerBottomEl.classList.toggle("active-turn", turn === bottomColor);
  if(mode === "ai"){
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Kompyuter o'ylanmoqda...";
  }else{
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Raqib navbati";
  }
}'''

new = '''function updateHeader(){
  const topName = myColor === "white" ? opponentName : currentUser;
  const bottomName = myColor === "white" ? currentUser : opponentName;
  const topColor = myColor === "white" ? "black" : "white";
  const bottomColor = myColor === "white" ? "white" : "black";
  if(pTopName) pTopName.textContent = escapeHtml(topName);
  if(pBotName) pBotName.textContent = escapeHtml(bottomName);
  if(pTopIcon) pTopIcon.textContent = topColor === "white" ? "\u2654" : "\u265a";
  if(pBotIcon) pBotIcon.textContent = bottomColor === "white" ? "\u2654" : "\u265a";
  playerTopEl.classList.toggle("active-turn", turn === topColor);
  playerBottomEl.classList.toggle("active-turn", turn === bottomColor);
  if(mode === "ai"){
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Kompyuter o'ylanmoqda...";
  }else{
    gameStatusEl.textContent = turn === myColor ? "Sizning navbatingiz" : "Raqib navbati";
  }
}'''
d = d.replace(old, new)

# 6. Add updateTimers in attemptMove
old = '    updateHeader();\n    if(mode === "ai"){ setTimeout(aiMove, 350); }'
new = '    updateHeader();\n    updateTimers();\n    if(mode === "ai"){ setTimeout(aiMove, 350); }'
d = d.replace(old, new)

# 7. Add stopTimer in leaveGame
old = 'leaveGameBtn.addEventListener("click", () => {\n  stopGamePoll();\n  if(chatBox) chatBox.classList.remove("active");'
new = 'leaveGameBtn.addEventListener("click", () => {\n  stopTimer();\n  stopGamePoll();\n  if(chatBox) chatBox.classList.remove("active");'
d = d.replace(old, new)

# 8. Add updateTimers in gameUpdate
old = '    case "gameUpdate":\n      if(currentGameId === msg.gameId){\n        pieces = msg.pieces;\n        turn = msg.turn;\n        drawBoard();\n        updateHeader();\n      }'
new = '    case "gameUpdate":\n      if(currentGameId === msg.gameId){\n        pieces = msg.pieces;\n        turn = msg.turn;\n        drawBoard();\n        updateHeader();\n        updateTimers();\n      }'
d = d.replace(old, new)

with open("c:/Users/MARUFXON/Desktop/12/app.js", "w", encoding="utf-8") as f:
    f.write(d)
print("All timer fixes applied, len:", len(d))
print("Parens:", d.count("(") == d.count(")"))
