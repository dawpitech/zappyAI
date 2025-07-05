from .look_action import LookAction
from .move_forward_action import MoveForwardAction
from .take_object_action import TakeObjectAction
from .turn_left_action import TurnLeftAction
from .turn_right_action import TurnRightAction

ACTIONS = [
    LookAction(),
    MoveForwardAction(),
    TakeObjectAction("food"),
    TurnRightAction(),
    TurnLeftAction()
]