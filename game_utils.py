import math
import pygame
from settings import *
from piece import Piece

from draw_utils import board_point_to_pixel
import random

# ==========================
# Bar / Tray Utilities
# ==========================
def player_has_bar(board, color):
    if color == "white":
        return len(board.white_tray) > 0
    else:
        return len(board.black_tray) > 0

def can_bear_off(board, color, start_index, step):
    """
    Ստուգում է՝ արդյոք հնարավոր է դուրս բերել քար:
    White: տախտակի 18-23 տողերում
    Black: տախտակի 0-5 տողերում
    """
    if color == "white":
        # White-ի համար տախտակի 0-17 հատվածում չպետք է մնա քարի
        for p in range(0, 18):
            if any(piece.color == "white" for piece in board.points[p].stack):
                return False
        return start_index + step >= 24
    else:
        for p in range(6, 24):
            if any(piece.color == "black" for piece in board.points[p].stack):
                return False
        return start_index - step < 0

# ==========================
# Game Start
# ==========================
def start_short_game(board):
    board.white_tray = [Piece("white") for _ in range(15)]
    board.black_tray = [Piece("black") for _ in range(15)]
    for point in board.points:
        point.stack.clear()
    return board

def start_long_game(board):
    board.white_tray = [Piece("white") for _ in range(15)]
    board.black_tray = [Piece("black") for _ in range(15)]
    for point in board.points:
        point.stack.clear()
    return board




def get_beaten_tray_position(color, RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK, index):
    """
    Սահմանում է խփված քարի ճիշտ դիրքը tray-ում
    index-ը՝ քանիերորդ քարն է tray-ում (stacking-ի համար)
    """
    offset = 18  # քարերի իրար վրա հեռավորությունը

    if color == "white":
        x = RIGHT_TRAY_WHITE.centerx
        y = RIGHT_TRAY_WHITE.top + 15 + index * offset
    else:
        x = RIGHT_TRAY_BLACK.centerx
        y = RIGHT_TRAY_BLACK.bottom - 15 - index * offset

    return pygame.Vector2(x, y)

# ==========================
# Get Valid Moves
# ==========================
def get_valid_moves(board, point_index, color, state):
    """
    Ստուգում է բոլոր հնարավոր moves՝ tray/bar-ից կամ խաղադաշտից
    """
    valid = []
    direction = 1 if color == "white" else -1

    tray = board.white_tray if color == "white" else board.black_tray

    # ==========================
    # BAR / TRAY ENTRY
    # ==========================
    if tray:
        for step in state["current_steps"]:
            if color == "white":
                enter_point = step - 1
                if enter_point > 5:
                    continue
            else:
                enter_point = 24 - step
                if enter_point < 18:
                    continue

            target_stack = board.points[enter_point].stack

            # ❌ արգելել միայն եթե 2+ հակառակորդ կա
            if len(target_stack) >= 2 and target_stack[-1].color != color:
                continue

            # ✅ մնացած դեպքերը՝ դատարկ, իր քարը, կամ 1 հակառակորդ → կարող է մտնել / hit անել
            valid.append(enter_point)

            print("BAR CHECK:",
                  "color =", color,
                  "dice =", step,
                  "enter_point =", enter_point,
                  "stack_len =", len(target_stack),
                  "top =", target_stack[-1].color if target_stack else None)

        return valid

    # ==========================
    # NORMAL MOVES
    # ==========================
    if point_index is not None and state["current_steps"]:
        for step in state["current_steps"]:
            target = point_index + step * direction
            if 0 <= target < 24:
                target_stack = board.points[target].stack

                # ❌ եթե 2+ թշնամի կա → փակ
                if len(target_stack) >= 2 and target_stack[-1].color != color:
                    continue

                # ✅ մնացած դեպքերը OK (դատարկ, իր քարը, 1 հակառակորդ → hit)
                valid.append(target)

            else:
                if can_bear_off(board, color, point_index, step):
                    valid.append("BEAR")

    return valid

# ==========================
# Move Piece
# ==========================
def move_piece(board, start_index, end, piece, state):
    """
    Իրականացնում է շարժումը՝ tray/bar → board, hit, normal moves, bear off
    """
    color = piece.color
    direction = 1 if color == "white" else -1

    if state.get("move_done_this_click"):
        return False

    # ==========================
    # Tray / BAR logic
    # ==========================
    if start_index is None:
        # Հանել քարը tray-ից և օգտագործել նույն object-ը
        if color == "white":
            piece = board.white_tray.pop()
        else:
            piece = board.black_tray.pop()

        step = get_enter_step(end, color)
        if step not in state["current_steps"]:
            return False
        state["current_steps"].remove(step)

    else:
        # NORMAL MOVE
        step = (end - start_index) if color == "white" else (start_index - end)
        if step not in state["current_steps"]:
            return False
        state["current_steps"].remove(step)
        board.points[start_index].stack.pop()

    # ==========================
    # Hit Logic նախքան քարը դնելը
    # ==========================
    if end != "BEAR":
        target_stack = board.points[end].stack
        if len(target_stack) == 1 and target_stack[-1].color != color:
            beaten = target_stack.pop()
            beaten.in_tray = True
            # ուղարկել tray
            if beaten.color == "white":
                index = len(board.white_tray)
                beaten.animation_pos = get_beaten_tray_position(
                    "white", RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK, index
                )
                board.white_tray.append(beaten)
            else:
                index = len(board.black_tray)
                beaten.animation_pos = get_beaten_tray_position(
                    "black", RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK, index
                )
                board.black_tray.append(beaten)

        # Տեղադրել քարը stack-ում
        board.points[end].stack.append(piece)
        piece.in_tray = False
        piece.animation_pos = None
    else:
        # ==========================
        # Bear Off
        # ==========================
        piece.in_tray = True
        piece.animation_pos = None

    # cleanup
    state["selected_piece"] = None
    state["valid_moves"] = []
    state["move_done_this_click"] = True

    
    return True
# ==========================
# Tray → Board step (enter)
# ==========================
def get_enter_step(end_index, color):
    if color == "white":
        return end_index + 1
    else:
        return 24 - end_index

# ==========================
# Animation
# ==========================
white_animation_queue = []
black_animation_queue = []

def animate_pieces_to_positions(board, RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK):
    global white_animation_queue, black_animation_queue
    white_animation_queue = []
    black_animation_queue = []

    positions = [
        (18, 5, "white"), 
        (16, 3, "white"), 
        (11, 5, "white"), 
        (0, 2, "white"),
        (12, 5, "black"), 
        (5, 5, "black"), 
        (7, 3, "black"), 
        (23, 2, "black")
    ]

    radius = 17
    overlap = radius

    for pos_index, count, color in positions:
        tray = board.white_tray if color == "white" else board.black_tray
        tray_rect = RIGHT_TRAY_WHITE if color == "white" else RIGHT_TRAY_BLACK
        x = tray_rect.centerx

        if color == "black":
            start_y = tray_rect.top + radius
            get_y = lambda i: start_y + i * overlap
        else:
            start_y = tray_rect.bottom - radius
            get_y = lambda i: start_y - i * overlap

        for i in range(count):
            if not tray:
                break
            piece = tray.pop()
            piece.in_tray = False
            start_pos = pygame.Vector2(x, get_y(i))
            piece.animation_pos = pygame.Vector2(start_pos)
            end_pos = pygame.Vector2(board_point_to_pixel(pos_index, 0))
            item = {"piece": piece, "start": start_pos, "end": end_pos, "end_index": pos_index, "t": 0.0}
            if color == "white":
                white_animation_queue.append(item)
            else:
                black_animation_queue.append(item)

def update_animation(dt, board):
    speed = 0.04 * dt
    arc_height = 40
    for queue in [white_animation_queue, black_animation_queue]:
        if not queue:
            continue
        item = queue[0]
        piece = item["piece"]
        start = item["start"]
        end = item["end"]
        t = item["t"]
        t += speed
        if t >= 1.0:
            t = 1.0
            piece.animation_pos = None
            board.points[item["end_index"]].stack.append(piece)
            queue.pop(0)
            continue
        ease_t = -0.5*math.cos(math.pi*t) + 0.5
        piece.animation_pos = start.lerp(end, ease_t)
        piece.animation_pos.y -= math.sin(math.pi*ease_t) * arc_height
        item["t"] = t

