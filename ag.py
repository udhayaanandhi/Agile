import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.agent_pos = [0, 0]  # Start at (0,0)
        self.gold_pos = None
        self.wumpus_pos = None
        self.pits = []
        self.is_alive = True
        self.has_gold = False
        self._generate_world()

    def _generate_world(self):
        # Randomly place Wumpus, Gold, and Pits (avoiding start)
        possible_cells = [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) != (0, 0)]
        
        self.wumpus_pos = random.choice(possible_cells)
        self.gold_pos = random.choice([c for c in possible_cells if c != self.wumpus_pos])
        
        # Each cell has 20% chance of being a pit
        for cell in possible_cells:
            if cell != self.wumpus_pos and cell != self.gold_pos:
                if random.random() < 0.2:
                    self.pits.append(cell)

    def get_percepts(self):
        r, c = self.agent_pos
        percepts = []
        
        # Check for Stench (adjacent to Wumpus)
        if any(abs(r-wr) + abs(c-wc) == 1 for wr, wc in [self.wumpus_pos]):
            percepts.append("Stench")
        
        # Check for Breeze (adjacent to Pit)
        if any(abs(r-pr) + abs(c-pc) == 1 for pr, pc in self.pits):
            percepts.append("Breeze")
            
        # Check for Glitter (on Gold)
        if (r, c) == self.gold_pos:
            percepts.append("Glitter")
            
        return percepts

    def move(self, action):
        r, c = self.agent_pos
        if action == "up" and r < self.size - 1: self.agent_pos[0] += 1
        elif action == "down" and r > 0: self.agent_pos[0] -= 1
        elif action == "right" and c < self.size - 1: self.agent_pos[1] += 1
        elif action == "left" and c > 0: self.agent_pos[1] -= 1
        
        # Check if agent died
        curr_pos = tuple(self.agent_pos)
        if curr_pos == self.wumpus_pos or curr_pos in self.pits:
            self.is_alive = False
            return "You died!"
        return f"Moved to {self.agent_pos}"

# --- Execution ---
game = WumpusWorld()
print(f"Start! Percepts: {game.get_percepts()}")
print(game.move("right"))
print(f"Current Percepts: {game.get_percepts()}")
