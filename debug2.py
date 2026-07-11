d = open("c:/Users/MARUFXON/Desktop/12/app.js", "r", encoding="utf-8").read()

cases = ["error", "registered", "users", "invite", "inviteSent", "inviteDeclined", "gameStart", "gameUpdate", "chat", "gameEnded"]
for c in cases:
    check = 'case "' + c + '"'
    found = check in d
    if not found:
        print("MISSING:", check)

print()
print("Total:", len(d), "chars")
print("Starts with IIFE:", d.startswith("(function"))
print("Ends with IIFE:", d.strip().endswith("})();"))
