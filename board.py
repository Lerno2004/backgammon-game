import random
import math

class Piece:
    def __init__(self, color, point_index=None):
        self.color = color              # "white" կամ "black"
        self.point_index = point_index  # 0–23
        self.radius = 19
        self.is_selected = False

        # animation
        self.animation_pos = None
        self.move_path = []

        # tray-ում է?
        self.in_tray = False

        # visual effect
        self.marble_lines = self.generate_marble_lines()
        self.highlight_angle = random.uniform(0, 2 * math.pi)

    def generate_marble_lines(self):
        lines = []
        for _ in range(random.randint(5, 10)):
            angle = random.uniform(0, 2 * math.pi)
            offset = random.uniform(0.3, 0.7)
            lines.append((angle, offset))
        return lines


class Point:
    def __init__(self, index):
        self.index = index
        self.stack = []

    def add(self, piece):
        piece.point_index = self.index
        self.stack.append(piece)

    def remove(self):
        if self.stack:
            return self.stack.pop()
        return None


class Board:
    def __init__(self):
        self.points = [Point(i) for i in range(24)]
        self.white_tray = []
        self.black_tray = []