# debug app.js

d = open("c:/Users/MARUFXON/Desktop/12/app.js", "r", encoding="utf-8").read()

# Check key functions
checks = [
    "function register",
    "function enterLobby",
    "function enterGame", 
    "function handleServerMessage",
    "playAiBtn.addEventListener",
    "case 'registered'",
    "case 'gameStart'",
    'sendToServer({ type: "register"',
    "connectWebSocket",
]

for c in checks:
    found = c in d
    print(f"  {c}: {'OK' if found else 'MISSING!'}")

# Find the register function
import re
lines = d.split("\n")
for i, l in enumerate(lines):
    if "function register" in l:
        print(f"\nRegister function at line {i}:")
        for j in range(i, min(i+20, len(lines))):
            print(f"  {j}: {lines[j]}")
        break

# Find handleServerMessage 
for i, l in enumerate(lines):
    if "function handleServerMessage" in l:
        print(f"\nhandleServerMessage at line {i}:")
        for j in range(i, min(i+30, len(lines))):
            print(f"  {j}: {lines[j]}")
        break
