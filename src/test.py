from planner import Planner
from actions.move_forward_action import MoveForwardAction
from actions.turn_left_action import TurnLeftAction
from actions.turn_right_action import TurnRightAction
from actions.take_object_action import TakeObjectAction
from actions.look_action import LookAction
from state import State
from goals.survive_goal import SurviveGoal
from local_map import LocalMap

# --- Setup initial ---
world_width = 5
world_height = 5
local_map = LocalMap(world_width, world_height)

initial_state = State(world_width=world_width, world_height=world_height)
initial_state["pos"] = (0, 0)
initial_state["dir"] = "E"
initial_state["inventory"] = {"food": 1260}
initial_state["map"] = local_map
initial_state["tick"] = 0

actions = [
    MoveForwardAction(),
    TurnLeftAction(),
    TurnRightAction(),
    TakeObjectAction("food"),
    LookAction()
]

goal = SurviveGoal()

planner = Planner(actions)

# --- Simuler un look ---
look_action = LookAction()
state_after_look = look_action.apply(initial_state.copy())

# Simuler la réponse du serveur au look, avec de la nourriture sur la tile (1,0)
fake_look_response = "[player, , , food]"  # suppose on regarde 5 tiles, la 1ere a de la food + player
state_after_look = look_action.update_map_from_look_response(state_after_look, fake_look_response)

print("Map tiles après look :")
for pos, tile in state_after_look["map"].tiles.items():
    print(f"Tile {pos}: stones={tile['stones']}, players={tile['players']}, last_seen={tile['last_seen']}")

# --- Planifier après mise à jour de la map ---
plan = planner.plan(state_after_look, goal)

if plan:
    print("\nPlan trouvé après look et mise à jour de carte :")
    for action in plan:
        print("-", action)
else:
    print("Aucun plan trouvé après mise à jour de la carte.")
