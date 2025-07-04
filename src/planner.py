import heapq

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def total_cost(self):
        return self.cost + self.heuristic

    def __lt__(self, other):
        return self.total_cost() < other.total_cost()


class Planner:
    def __init__(self, actions):
        self.actions = actions

    def heuristic(self, state, goal):
        if hasattr(goal, "heuristic"):
            return goal.heuristic(state)
        return 0

    def plan(self, start_state, goal, max_iterations=1000):
        goal.update_priority(start_state)

        if not goal.is_reached(start_state):
            if hasattr(goal, "get_subgoal"):
                subgoal = goal.get_subgoal(start_state)
                if subgoal:
                    return self.plan(start_state, subgoal, max_iterations)

            if hasattr(goal, "get_desired_state"):
                desired_state = goal.get_desired_state(start_state)
                if desired_state is None:
                    return None
            else:
                desired_state = None
        else:
            return []

        open_list = []
        closed_set = set()

        start_node = Node(state=start_state, cost=0, heuristic=self.heuristic(start_state, goal))
        heapq.heappush(open_list, start_node)

        iterations = 0

        while open_list and iterations < max_iterations:
            current_node = heapq.heappop(open_list)
            current_state_tuple = current_node.state.to_tuple()

            if current_state_tuple in closed_set:
                continue
            closed_set.add(current_state_tuple)

            if goal.is_reached(current_node.state):
                return self.reconstruct_plan(current_node)

            for action in self.actions:
                if not action.is_applicable(current_node.state):
                    continue

                new_state = action.apply(current_node.state)
                new_cost = current_node.cost + action.compute_cost(current_node.state)
                heuristic = self.heuristic(new_state, goal)
                new_node = Node(new_state, current_node, action, new_cost, heuristic)

                heapq.heappush(open_list, new_node)

            iterations += 1

        return None

    def reconstruct_plan(self, node):
        actions = []
        while node.parent:
            actions.insert(0, node.action)
            node = node.parent
        return actions
