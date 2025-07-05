import sys

class Agent:
    def __init__(self, initial_state, planner):
        self.state = initial_state
        self.planner = planner

        self.goal = None
        self.current_plan = []
        self.current_action = None
        self.waiting_for_response = False

        self.inbox = []
        self.command_queue = []

    def set_goal(self, goal):
        self.goal = goal
        self.current_plan = []
        self.current_action = None

    def receive_message(self, message):
        self.inbox.append(message.strip())
        self.waiting_for_response = False

    def tick(self):
        if self.waiting_for_response:
            return

        while self.inbox:
            msg = self.inbox.pop(0)
            self.handle_response(msg)

        if not self.current_plan and self.goal:
            self.current_plan = self.planner.plan(self.state, self.goal)
            if not self.current_plan:
                print("[WARN] Aucun plan trouvé", file=sys.stderr)
                return

        if self.current_plan:
            self.current_action = self.current_plan.pop(0)
            self.current_action.execute(self)
            self.waiting_for_response = True

    def handle_response(self, message):
        # print(f"[RECV] {message}", file=sys.stderr)

        if message.startswith("message"):
            direction, text = self.parse_broadcast(message)
            self.handle_broadcast(direction, text)
            return

        if message.startswith("eject:"):
            direction = int(message.split(":")[1].strip())
            self.handle_eject(direction)
            return

        if message == "ko":
            print(f"[WARN] Action échouée : {self.current_action}", file=sys.stderr)
            if self.current_action:
                self.state["tick"] += self.current_action.cost
                self.state["inventory"]["food"] = max(0, self.state["inventory"].get("food", 0) - self.current_action.cost)
            self.reset_action_state()
            self.current_plan = []
            return

        if self.current_action:
            try:
                if hasattr(self.current_action, "apply_agent"):
                    self.state = self.current_action.apply_agent(self.state, message)
                else:
                    self.state = self.current_action.apply(self.state)
            except Exception as e:
                print(f"[ERROR] Erreur durant apply_agent/apply : {e}", file=sys.stderr)
            self.reset_action_state()
        else:
            print("[WARN] Réponse reçue mais aucune action en cours", file=sys.stderr)

    def reset_action_state(self):
        self.current_action = None
        self.waiting_for_response = False

    def parse_broadcast(self, message):
        parts = message[len("message"):].split(",", 1)
        direction = int(parts[0].strip())
        text = parts[1].strip()
        return direction, text

    def handle_broadcast(self, direction, text):
        print(f"[INFO] Broadcast ignoré : {direction} => {text}", file=sys.stderr)

    def handle_eject(self, direction):
        print(f"[INFO] Eject depuis la direction {direction} (non géré)", file=sys.stderr)

    def next_command(self):
        return self.command_queue.pop(0) if self.command_queue else None

    def has_command(self):
        return bool(self.command_queue)

    def queue_command(self, command):
        self.command_queue.append(command)
