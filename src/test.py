from state import State

etat = State()
print(etat)
etat["level"] += 1
print("Nouveau niveau :", etat["level"])
print(etat)