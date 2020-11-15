import random


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def get_direction(curr, dest):
    delta_x = clamp(dest['x'] - curr['x'], -1, 1)
    delta_y = clamp(dest['y'] - curr['y'], -1, 1)
    if random.random() < 0.5:
        if delta_x != 0:
            delta_y = 0
    else:
        if delta_y != 0:
            delta_x = 0
            
    return (delta_x, delta_y)


def position_equals(a, b):
    return a["x"] == b["x"] and a["y"] == b["y"]

def random_move():
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    return directions[random.randrange(len(directions))]

def compute_distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])
