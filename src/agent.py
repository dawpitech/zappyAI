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
        self.outbox = []
        self.command_queue = []

    def set_goal(self, goal):
        self.goal = goal
        self.current_plan = []
        self.current_action = None

    def receive_message(self, message):
        self.inbox.append(message.strip())

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
        if message.startswith("message"):
            direction, text = self.parse_broadcast(message)
            self.handle_broadcast(direction, text)
            return

        if message.startswith("eject:"):
            direction = int(message.split(":")[1].strip())
            self.handle_eject(direction)
            return

        if self.current_action:
            self.state = self.current_action.apply_agent(self.state, message)
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
        return len(self.command_queue) > 0

    def queue_command(self, command):
        self.command_queue.append(command)
