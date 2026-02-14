import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.agent_pos = [0, 0]   # Start position
        self.gold_pos = None
        self.wumpus_pos = None
        self.pits = []
        self.is_alive = True
        self.has_gold = False
        self._generate_world()

    # -----------------------------
    # Generate World
    # -----------------------------
    def _generate_world(self):
        possible_cells = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if (r, c) != (0, 0)
        ]

        self.wumpus_pos = random.choice(possible_cells)
        self.gold_pos = random.choice(
            [c for c in possible_cells if c != self.wumpus_pos]
        )

        # 20% probability for pits
        for cell in possible_cells:
            if cell != self.wumpus_pos and cell != self.gold_pos:
                if random.random() < 0.2:
                    self.pits.append(cell)

    # -----------------------------
    # Percepts
    # -----------------------------
    def get_percepts(self):
        r, c = self.agent_pos
        percepts = []

        # Stench near Wumpus
        wr, wc = self.wumpus_pos
        if abs(r - wr) + abs(c - wc) == 1:
            percepts.append("Stench")

        # Breeze near Pit
        for pr, pc in self.pits:
            if abs(r - pr) + abs(c - pc) == 1:
                percepts.append("Breeze")
                break

        # Glitter on Gold
        if (r, c) == self.gold_pos:
            percepts.append("Glitter")

        return percepts

    # -----------------------------
    # Agent Movement
    # -----------------------------
    def move(self, action):
        if not self.is_alive:
            return "Agent is dead!"

        r, c = self.agent_pos

        if action == "up" and r < self.size - 1:
            self.agent_pos[0] += 1
        elif action == "down" and r > 0:
            self.agent_pos[0] -= 1
        elif action == "right" and c < self.size - 1:
            self.agent_pos[1] += 1
        elif action == "left" and c > 0:
            self.agent_pos[1] -= 1
        else:
            return "Invalid move!"

        curr_pos = tuple(self.agent_pos)

        # Death conditions
        if curr_pos == self.wumpus_pos:
            self.is_alive = False
            return "You were eaten by the Wumpus!"

        if curr_pos in self.pits:
            self.is_alive = False
            return "You fell into a pit!"

        return f"Moved to {self.agent_pos}"

    # -----------------------------
    # Grab Gold
    # -----------------------------
    def grab_gold(self):
        if tuple(self.agent_pos) == self.gold_pos:
            self.has_gold = True
            return "Gold collected!"
        return "No gold here."

    # -----------------------------
    # Display Grid (for debugging)
    # -----------------------------
    def show_world(self):
        print("\nWorld Layout (Debug View)")
        for r in range(self.size):
            row = ""
            for c in range(self.size):
                cell = "."
                if (r, c) == tuple(self.agent_pos):
                    cell = "A"
                elif (r, c) == self.gold_pos:
                    cell = "G"
                elif (r, c) == self.wumpus_pos:
                    cell = "W"
                elif (r, c) in self.pits:
                    cell = "P"
                row += cell + " "
            print(row)


# -----------------------------
# Execution
# -----------------------------
if __name__ == "__main__":
    game = WumpusWorld()

    game.show_world()

    print("\nStart Percepts:", game.get_percepts())

    print(game.move("right"))
    print("Percepts:", game.get_percepts())

    print(game.move("up"))
    print("Percepts:", game.get_percepts())

    print(game.grab_gold())
