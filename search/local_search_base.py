import random


class LocalSearchBase:
    def __init__(self, world):
        self.world = world
        self.targets = self.world.get_targets()

    def get_random_valid_pos(self):
        while True:
            x = random.randint(0, self.world.rows - 1)
            y = random.randint(0, self.world.cols - 1)
            if self.world.is_valid_position(x, y):
                return (x, y)

    def initialize_state(self):
        num_sensors = random.randint(1, self.world.max_sensors)
        initial_state = set()
        while len(initial_state) < num_sensors:
            initial_state.add(self.get_random_valid_pos())
        return list(initial_state)

    def evaluate(self, state):
        covered = set()
        for sx, sy in state:
            for tx, ty in self.targets:
                if (tx, ty) not in covered:
                    if abs(sx - tx) + abs(sy - ty) <= self.world.sensor_range:
                        covered.add((tx, ty))
        
        uncovered_count = len(self.targets) - len(covered)
        return (uncovered_count * 1000) + len(state)

    def get_neighbor(self, state):
        if not state:
            return [self.get_random_valid_pos()]
            
        neighbor = list(state)
        ops = ['move', 'add', 'remove']
        weights = [0.6, 0.2, 0.2] 
        
        if len(neighbor) >= self.world.max_sensors:
            ops = ['move', 'remove']
            weights = [0.7, 0.3]
        elif len(neighbor) <= 1:
            ops = ['move', 'add']
            weights = [0.7, 0.3]
            
        op = random.choices(ops, weights=weights, k=1)[0]
        
        if op == 'move':
            idx = random.randint(0, len(neighbor) - 1)
            old_pos = neighbor[idx]
            
            if random.random() < 0.3:
                neighbor[idx] = self.get_random_valid_pos()
            else:
                moves = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                random.shuffle(moves)
                moved = False
                for dx, dy in moves:
                    nx, ny = old_pos[0] + dx, old_pos[1] + dy
                    if self.world.is_valid_position(nx, ny):
                        neighbor[idx] = (nx, ny)
                        moved = True
                        break
                if not moved:
                    neighbor[idx] = self.get_random_valid_pos()
                    
        elif op == 'add':
            neighbor.append(self.get_random_valid_pos())
        elif op == 'remove':
            idx = random.randint(0, len(neighbor) - 1)
            neighbor.pop(idx)
            
        return list(set(neighbor))
