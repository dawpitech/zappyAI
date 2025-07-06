from .look_action import LookAction
from .move_forward_action import MoveForwardAction
from .take_object_action import TakeObjectAction
from .turn_left_action import TurnLeftAction
from .turn_right_action import TurnRightAction
from .incantation_action import IncantationAction
from .drop_object_action import DropObjectAction

ACTIONS = [
    LookAction(),
    MoveForwardAction(),
    # DropObjectAction("linemate"),
    # DropObjectAction("deraumere"),
    # DropObjectAction("sibur"),
    # DropObjectAction("mendiane"),
    # DropObjectAction("phiras"),
    # DropObjectAction("thystame"),
    TakeObjectAction("food"),
    # TakeObjectAction("linemate"),
    # TakeObjectAction("deraumere"),
    # TakeObjectAction("sibur"),
    # TakeObjectAction("mendiane"),
    # TakeObjectAction("phiras"),
    # TakeObjectAction("thystame"),
    # IncantationAction(),
    TurnRightAction(),
    TurnLeftAction()
]