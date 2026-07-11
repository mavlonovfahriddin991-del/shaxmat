# Final fix for deploy
d = open("c:/Users/MARUFXON/Desktop/Farhodov/app.js", "r", encoding="utf-8").read()

# 1. Fix WebSocket connect
old_ws = 'ws = new WebSocket(proto + "//" + host);'
new_ws = 'ws = new WebSocket(proto + "//" + host + window.location.pathname);'
if old_ws in d:
    d = d.replace(old_ws, new_ws)

# 2. Fix duplicate chat case - check count
import re
matches = list(re.finditer('case "chat"', d))
count = len(matches)
if count > 1:
    print("Found", count, "chat cases, fixing...")
    # Find the start of the second duplicate
    second_start = matches[1].start()
    # Find next case after it
    next_case = d.find('case "gameEnded"', second_start)
    if next_case > 0:
        # Remove from second case to before gameEnded
        d = d[:second_start] + d[next_case:]

# 3. Verify structure
chat_count = len(re.findall('case "chat"', d))
print("Chat cases after fix:", chat_count)

with open("c:/Users/MARUFXON/Desktop/12/app.js", "w", encoding="utf-8") as f:
    f.write(d)
print("app.js written:", len(d), "chars")
