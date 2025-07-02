from state import State
from actions.move_forward_action import MoveForwardAction
from actions.turn_left_action import TurnLeftAction
from actions.turn_right_action import TurnRightAction

etat = State()
print(etat)
etat["level"] += 1
print("Nouveau niveau :", etat["level"])
print(etat)