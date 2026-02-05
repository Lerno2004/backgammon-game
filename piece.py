#Քար + նկարում
import pygame
import math
import random

class Piece:
    def __init__(self, color, point_index=None):
        self.color = color             # "white" կամ "black"
        self.point_index = point_index # Քարի դիրքը տախտակի վրա,0–23 (թե որ եռանկյունում է գտնվում)
        self.radius = 22           # Քարի ֆիզիկական չափը
        self.is_selected = False       # Ընտրված է՞ մկնիկով,True եթե խաղացողը սեղմել է վրա
        self.animation_pos = None      # pixel դիրք animation-ի համար,եթե քարը շարժվում է, այստեղ պահվում է նրա ընթացիկ pixel դիրքը
        self.move_path = []            # pixel coordinates՝ animation-ի համար,շարժման ճանապարհ (start → end pixel)
        self.in_tray = False           # Ամանի մեջ է,True եթե քարը դուրս է բերվել
        # Քարի չափ ըստ գույնի
        

        # Dragging support
        self.dragging = False
        self.drag_offset = (0, 0)

        # Նատուրալ էֆեկտների համար
        self.marble_lines = self.generate_marble_lines()
        self.highlight_angle = random.uniform(0, 2*math.pi)
        
    
    def generate_marble_lines(self):
        """Հետաքրքիր տարբերակ՝ բնական մարմարի effect"""
        lines = []
        num_lines = random.randint(5, 10)
        for i in range(num_lines):
            angle = random.uniform(0, 2*math.pi)
            offset = random.uniform(0.3, 0.7)
            lines.append((angle, offset))
        return lines

class Point:
    def __init__(self, index):
        self.index = index
        self.stack = []

    def add(self, piece):
        self.stack.append(piece)

    def remove(self):
        if self.stack:
            return self.stack.pop()
        return None
    
class Board:
    def __init__(self):
        self.points = [Point(i) for i in range(24)] #24 օբյեկտ (Point), որտեղ պահվում են բոլոր քարերը
        self.white_tray = [] #“աման”, որտեղ դրվում են սպիտակների հարվածված քարերը
        self.black_tray = [] #նույնը սևերի համար