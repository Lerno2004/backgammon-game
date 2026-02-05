import sys
import math 
import random
import pygame
from  random import uniform

pygame.init() #միացնում է Pygame-ի բոլոր մոդուլները
WIDTH,HEIGHT=1000,600 #պատուհանի չափը՝ 1000×600
BOARD_X=100 #տախտակը գծելու դիրքը՝ (x->100, y->50)
BOARD_Y=50
BOARD_WIDTH=800#տախտակի չափը՝ 800×500
BOARD_HEIGHT=500
screen=pygame.display.set_mode((WIDTH,HEIGHT)) #ստեղծում ա պատուհան 1000,600
pygame.display.set_caption("Nardi Step 1-Window")
Wood=(122, 196, 153)#փայտի շականակագույն
BG_COLOR=(122, 196, 153)# բաց շականակագույն
BROWN=(0, 81, 163)#մուգ շականակագույն
CREAM=(140, 194, 255)#մարմնագույն
WHITE = (255, 255, 255)
LIGHT_WOOD=(237, 244, 255)
DARK_BROWN=(41, 75, 120)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

wood_texture = pygame.image.load("/Users/lernikpetrosyan/Desktop/Brown Wood Texture_276_2048.jpg").convert()
wood_texture = pygame.transform.scale(wood_texture, (WIDTH, HEIGHT))


board_texture = pygame.image.load("/Users/lernikpetrosyan/Desktop/Birch Wood Texture_285_2048 2.jpg").convert()
board_texture = pygame.transform.scale(board_texture, (BOARD_WIDTH, BOARD_HEIGHT))

triangle_width=BOARD_WIDTH/12# 12 երանկյուն տեղավորվի մի տախտակի մեջ(տախտակի լայնությունը / 12)
triangle_height = BOARD_HEIGHT // 3# բարձրություն երանկյան գտնվելու,վերևի/ստորին հատվածի բարձրությունը
line_height = 20
line_width = 2
LEFT_TRAY = pygame.Rect(20, 200, 60, 200)
RIGHT_TRAY = pygame.Rect(WIDTH-80, 200, 60, 200)

# Պոսիկների լայնք ու տարածք
TRAY_WIDTH = 40
TRAY_SPACING = 15
# Պոսիկների ուղղանկյունները (երկուսն էլ աջ կողմում, կողք-կողքի, վերևից ներքև)
RIGHT_TRAY_WHITE = pygame.Rect(
    BOARD_X + BOARD_WIDTH + TRAY_SPACING,  # տախտակից աջ կողմ
    BOARD_Y,                              # վերևից տախտակի նույն դիրքը
    TRAY_WIDTH,
    BOARD_HEIGHT // 2 - TRAY_SPACING // 2  # բարձրությունը կեսն է, ափսենում փոքր ընդմիջում
)

RIGHT_TRAY_BLACK = pygame.Rect(
    BOARD_X + BOARD_WIDTH + TRAY_SPACING,
    BOARD_Y + BOARD_HEIGHT // 2 + TRAY_SPACING // 2,  # կեսից ներքև
    TRAY_WIDTH,
    BOARD_HEIGHT // 2 - TRAY_SPACING // 2)

#“Կարճ խաղ” և “Երկար խաղ” կոճակներ
short_button = pygame.Rect(420, 10, 160, 40)  
long_button  = pygame.Rect(600, 10, 160, 40)

triangle_texture = pygame.image.load("/Users/lernikpetrosyan/Desktop/walnut-wood-texture-.jpg").convert()
triangle_texture = pygame.transform.scale(triangle_texture, (int(triangle_width), int(triangle_height)))


frame_texture = pygame.image.load("/Users/lernikpetrosyan/Desktop/walnut-wood-texture-.jpg").convert()
frame_texture = pygame.transform.scale(frame_texture, (BOARD_WIDTH+30, BOARD_HEIGHT+30))



# Քառակուսիների չափերը (օրինակ, 12 քառակուսի աջ կամ ստորին շարքում)
SQUARE_WIDTH = BOARD_WIDTH // 12   # 12 քառակուսի լայնությունը տախտակի վրա
SQUARE_HEIGHT = BOARD_HEIGHT // 3  # քառակուսու բարձրությունը, ըստ այն հատվածի


DICE_SIZE = 40 #մեկ զարի նկարի չափը՝ 50×50 px
FPS = 60 #խաղի refresh արագությունը (60 frame/sec)
clock = pygame.time.Clock()

# Ներբեռնում ենք զարերի PNG պատկերները 1-ից 6
dice_textures = [pygame.image.load(f"/Users/lernikpetrosyan/Desktop/dice_faces_hd/{i}_dots.png").convert_alpha() for i in range(1,7)]
for i in range(6):
    dice_textures[i] = pygame.transform.scale(dice_textures[i], (DICE_SIZE, DICE_SIZE))


def compute_steps():
    global current_steps, dice_list

    # համոզվել, որ value-ներն արդեն հասանելի են
    if dice_list[0].value is None or dice_list[1].value is None:
        return

    d1 = dice_list[0].value
    d2 = dice_list[1].value

    if d1 == d2:
        current_steps = [d1]*4
    else:
        current_steps = [d1, d2]


selected_piece = None
selected_index = None
valid_moves=[]
class Piece:
    def __init__(self, color, point_index=None):
        self.color = color             # "white" կամ "black"
        self.point_index = point_index # Քարի դիրքը տախտակի վրա,0–23 (թե որ եռանկյունում է գտնվում)
        self.radius = 19               # Քարի ֆիզիկական չափը
        self.is_selected = False       # Ընտրված է՞ մկնիկով,True եթե խաղացողը սեղմել է վրա
        self.animation_pos = None      # pixel դիրք animation-ի համար,եթե քարը շարժվում է, այստեղ պահվում է նրա ընթացիկ pixel դիրքը
        self.move_path = []            # pixel coordinates՝ animation-ի համար,շարժման ճանապարհ (start → end pixel)
        self.in_tray = False           # Ամանի մեջ է,True եթե քարը դուրս է բերվել
        
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

class Board:
    def __init__(self):
        self.points = [Point(i) for i in range(24)] #24 օբյեկտ (Point), որտեղ պահվում են բոլոր քարերը
        self.white_tray = [] #“աման”, որտեղ դրվում են սպիտակների հարվածված քարերը
        self.black_tray = [] #նույնը սևերի համար

#Dice class (շարժում + գնալ դեպի նպատակային դիրք)
class Dice:
    def __init__(self, start_pos):
        self.pos = pygame.Vector2(start_pos)
        self.target = pygame.Vector2(start_pos)
        self.value = None          # դեռ value չկա
        self.is_rolling = False
        self.roll_time = 0
        self.velocity = pygame.Vector2(0,0)

    def roll(self):
        self.is_rolling = True
        self.roll_time = 0
        self.value = None          # ջնջում ենք հին value
        global white_turn
        x_vel = -random.uniform(6,12) if white_turn else random.uniform(6,12)
        y_vel = -random.uniform(10,15)
        self.velocity = pygame.Vector2(x_vel, y_vel)

    def update(self, dt):
        global dice_ready, current_steps

        if self.is_rolling:
            self.roll_time += dt
            self.velocity.y += 0.5
            self.pos += self.velocity

            # Հողի հետ բախում
            if self.pos.y >= self.target.y:
                self.pos.y = self.target.y
                self.velocity.y *= -0.3

                if abs(self.velocity.y) < 1:
                    self.is_rolling = False
                    self.velocity = pygame.Vector2(0, 0)
                    self.value = random.randint(1,6)   # value տրվում է միայն կանգնելու պահին

        else:
            # Հարթ շարժում դեպի նպատակային դիրք
            self.pos += (self.target - self.pos) * 0.1

        # Ստուգում՝ բոլորը կանգնած են → հաշվարկել steps
        if (
            not dice_ready
            and all(not d.is_rolling for d in dice_list)
            and all(d.value is not None for d in dice_list)
        ):
            compute_steps()
            dice_ready = True

    def draw(self, screen):
        if self.is_rolling:
            # ցուցադրել «պտտվող» զար
            random_value = random.randint(1,6)
            screen.blit(dice_textures[random_value-1], self.pos)
        elif self.value is not None:
            # վերջնական value
            screen.blit(dice_textures[self.value-1], self.pos)

current_steps = []        # օրվա զարերը (օր. [3,6] կամ [4,4,4,4])
dice_ready = False        # զարերը կանգնեցին
must_enter = False        # խաղացողը ունի հարվածված քար tray-ում
game_over = False         # հաղթանակի վիճակ
dice_list = [Dice((200, 250)), Dice((300, 250))]
white_turn = True
# Հերթ փոխելու ֆունկցիա
def change_turn():
    global white_turn, dice_ready, current_steps

    white_turn = not white_turn
    current_steps = []
    dice_ready = False

    # ջնջել հին value-ները և կանգնեցնել զարերը
    for d in dice_list:
        d.value = None
        d.is_rolling = False
        d.roll_time = 0

    roll_dice_for_turn()

def roll_dice_for_turn():
    global dice_ready

    dice_ready = False
    start_x = 200 if white_turn else 700
    y = 250
    for i, dice in enumerate(dice_list):
        dice.target = pygame.Vector2(start_x + i*100, y)
        dice.roll() 

def draw_board():
    screen.blit(wood_texture, (0, 0))
    
    FRAME_COLOR = (160, 82, 45)
    frame_rect = pygame.Rect(BOARD_X-15, BOARD_Y-15, BOARD_WIDTH+30, BOARD_HEIGHT+30)
    pygame.draw.rect(screen, FRAME_COLOR, frame_rect)
    
    LIGHT_EDGE = (185, 122, 87)
    DARK_EDGE = (110, 50, 30)
    pygame.draw.line(screen, LIGHT_EDGE, (frame_rect.left, frame_rect.top), (frame_rect.right, frame_rect.top), 3)
    pygame.draw.line(screen, LIGHT_EDGE, (frame_rect.left, frame_rect.top), (frame_rect.left, frame_rect.bottom), 3)
    pygame.draw.line(screen, DARK_EDGE, (frame_rect.left, frame_rect.bottom-1), (frame_rect.right, frame_rect.bottom-1), 3)
    pygame.draw.line(screen, DARK_EDGE, (frame_rect.right-1, frame_rect.top), (frame_rect.right-1, frame_rect.bottom), 3)
    
    screen.blit(board_texture, (BOARD_X, BOARD_Y))
    
    center_x = BOARD_X + BOARD_WIDTH // 2
    DARK_TRIANGLE = (145, 106, 73)
    LIGHT_TRIANGLE = (179, 137, 93)
    alpha = 150  # Թափանցիկություն

    def draw_triangle(points, color, alpha=150):
        # Գտնում ենք եռանկյան սահմանները
        min_x = min(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)
        width = max_x - min_x
        height = max_y - min_y

        # Փոքր surface հենց եռանկյան համար
        tri_surf = pygame.Surface((int(width)+1, int(height)+1), pygame.SRCALPHA)
        adjusted_points = [(p[0]-min_x, p[1]-min_y) for p in points]
        pygame.draw.polygon(tri_surf, (*color, alpha), adjusted_points)
        screen.blit(tri_surf, (min_x, min_y))

    # Ձախ վերև
    for i in range(6):
        x0 = BOARD_X + i * triangle_width
        color = LIGHT_TRIANGLE if i % 2 == 0 else DARK_TRIANGLE
        points = [(x0, BOARD_Y), (x0 + triangle_width, BOARD_Y), (x0 + triangle_width/2, BOARD_Y + triangle_height)]
        draw_triangle(points, color, alpha)

    # Ձախ ներքև
    for i in range(6):
        x0 = BOARD_X + i * triangle_width
        color = LIGHT_TRIANGLE if i % 2 == 0 else DARK_TRIANGLE
        y0 = BOARD_Y + BOARD_HEIGHT
        points = [(x0, y0), (x0 + triangle_width, y0), (x0 + triangle_width/2, y0 - triangle_height)]
        draw_triangle(points, color, alpha)

    # Աջ վերև
    for i in range(6):
        x0 = center_x + i * triangle_width
        color = DARK_TRIANGLE if i % 2 == 0 else LIGHT_TRIANGLE
        points = [(x0, BOARD_Y), (x0 + triangle_width, BOARD_Y), (x0 + triangle_width/2, BOARD_Y + triangle_height)]
        draw_triangle(points, color, alpha)

    # Աջ ներքև
    for i in range(6):
        x0 = center_x + i * triangle_width
        color = DARK_TRIANGLE if i % 2 == 0 else LIGHT_TRIANGLE
        y0 = BOARD_Y + BOARD_HEIGHT
        points = [(x0, y0), (x0 + triangle_width, y0), (x0 + triangle_width/2, y0 - triangle_height)]
        draw_triangle(points, color, alpha)

    # Կենտրոնական գիծ
    line_width = 9
    pygame.draw.rect(screen, FRAME_COLOR, (center_x - line_width//2, BOARD_Y, line_width, BOARD_HEIGHT))
    pygame.draw.line(screen, LIGHT_EDGE, (center_x - line_width//2, BOARD_Y), 
                     (center_x - line_width//2, BOARD_Y + BOARD_HEIGHT), 2)
    pygame.draw.line(screen, DARK_EDGE, (center_x + line_width//2 - 1, BOARD_Y), 
                     (center_x + line_width//2 - 1, BOARD_Y + BOARD_HEIGHT), 2)

animation_angle=0
def draw_piece(x, y, piece: Piece):
    radius = 17
    if piece.animation_pos is not None:
        x, y = piece.animation_pos

    # Ստվերի գույն
    if piece.color == "white":
        shadow_color = (204, 189, 182, 110)
    else:
        shadow_color = (0, 0, 0, 180)
    pygame.draw.circle(screen, shadow_color, (x + 3, y + 3), radius)

    # Pixel մակերես
    piece_surf = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
    piece_surf.fill((0, 0, 0, 0))

    # Հիմնական գույն
    base_color = (240, 230, 220) if piece.color == "white" else (60, 40, 30)
    pygame.draw.circle(piece_surf, base_color, (radius+2, radius+2), radius)

    # Եզրագիծ
    border_color = (179, 161, 139) if piece.color == "white" else (40, 20, 10)
    pygame.draw.circle(piece_surf, border_color, (radius+2, radius+2), radius, 2)

    # Եթե քարը ընտրված է՝ կանաչ շրջանակ
    if piece.is_selected:
        pygame.draw.circle(piece_surf, (0, 255, 0, 150), (radius+2, radius+2), radius+2, 3)

    # Էկրանին տեղադրում
    screen.blit(piece_surf, (x - radius - 2, y - radius - 2))


# Ստանալ կետի index-ը ըստ մկնիկի դիրքի
def get_point_index(mx, my):
    if not (BOARD_X <= mx <= BOARD_X + BOARD_WIDTH):
        return None
    if not (BOARD_Y <= my <= BOARD_Y + BOARD_HEIGHT):
        return None

    local_x = mx - BOARD_X
    triangle = int(local_x // triangle_width)  # <<< ապահով integer

    if my < BOARD_Y + BOARD_HEIGHT // 2:
        return triangle
    else:
        return 23 - triangle

# Քարերի նկարումը ըստ points[] զանգվածի
# 3️⃣ Քարերի նկարում
# ------------------------------
def draw_all_pieces():
    # Նկարել տախտակի stack-երը
    for point in board.points:
        for i, piece in enumerate(point.stack):
            pos = piece.animation_pos if piece.animation_pos else board_point_to_pixel(point.index, i)
            draw_piece(int(pos[0]), int(pos[1]), piece)
    # Նկարել animation queue-ում եղած քարերը
    for queue in [white_animation_queue, black_animation_queue]:
        for item in queue:
            piece = item["piece"]
            draw_piece(int(piece.animation_pos.x), int(piece.animation_pos.y), piece)

font = pygame.font.Font("NotoSansArmenian-VariableFont_wdth,wght.ttf", 5)  
def draw_buttons():
    pygame.draw.rect(screen, (40, 40, 40), short_button, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), long_button, border_radius=8)

    short_text = font.render("Կարճ խաղ", True, WHITE)
    long_text  = font.render("Երկար խաղ", True, WHITE)

    # Կենտրոնացնենք տեքստը կոճակի մեջ
    short_text_rect = short_text.get_rect(center=short_button.center)
    long_text_rect  = long_text.get_rect(center=long_button.center)

    screen.blit(short_text, short_text_rect)
    screen.blit(long_text, long_text_rect)

# Գրաֆիկ ֆունկցիա՝ պոսիկները գծելու համար
def draw_right_trays(screen):
    # Պոսիկների ֆոն (կապույտ, քո ուզած գույնով)
    tray_color = (0, 40, 80)  # Կապույտ մուգ երանգ

    pygame.draw.rect(screen, tray_color, RIGHT_TRAY_WHITE, border_radius=8)
    pygame.draw.rect(screen, tray_color, RIGHT_TRAY_BLACK, border_radius=8)

# Քարերի դասավորումը պոսիկներում (ներառենք օրինակ)
def draw_pieces_in_tray(screen, pieces, tray_rect):
    piece_radius = 17
    overlap = piece_radius  # overlapped overlapped

    x = tray_rect.centerx
    start_y = tray_rect.top + piece_radius

    # Դրանց նկարում ենք reversed order — վերջինը (ավելի նոր) կլինի վերևում
    for i, piece in enumerate(reversed(pieces)):
        y = start_y + i * overlap
        # եթե piece-ի animation_pos կա՝ նկարի այն դիրքով, հատուկ տարրեր հաշվի առ:
        if getattr(piece, "animation_pos", None) is not None:
            px, py = int(piece.animation_pos.x), int(piece.animation_pos.y)
            draw_piece(px, py, piece)
        else:
            draw_piece(int(x), int(y), piece)
# Օրինակ՝ խաղի լիցքավորման ժամանակ քարի տիրույթները տրաներում պահենք
# board.white_tray և board.black_tray քո մեջ արդեն կան

# Գլխավոր նկարչական ֆունկցիայի մեջ կանչենք

def draw_trays_and_pieces(screen, board):
    draw_right_trays(screen)
    draw_pieces_in_tray(screen, board.white_tray, RIGHT_TRAY_WHITE)
    draw_pieces_in_tray(screen, board.black_tray, RIGHT_TRAY_BLACK)


def draw_buttons():
    pygame.draw.rect(screen, (40, 40, 40), short_button, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), long_button, border_radius=8)

    font_name = "NotoSansArmenian-VariableFont_wdth,wght.ttf"
    
    def render_text_fit(button, text):
        font_size = 32  # ամեն անգամ նորից սկսում
        font = pygame.font.Font(font_name, font_size)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect()

        while (text_rect.width > button.width - 10 or text_rect.height > button.height - 10) and font_size > 10:
            font_size -= 1
            font = pygame.font.Font(font_name, font_size)
            text_surf = font.render(text, True, WHITE)
            text_rect = text_surf.get_rect()

        text_rect.center = button.center
        return text_surf, text_rect

    short_text_surf, short_text_rect = render_text_fit(short_button, "Կարճ խաղ")
    long_text_surf, long_text_rect   = render_text_fit(long_button, "Երկար խաղ")

    screen.blit(short_text_surf, short_text_rect)
    screen.blit(long_text_surf, long_text_rect)

    
def start_short_game():
    global board
    board = Board()

    # Ամանի մեջ տեղավորում ենք բոլոր քարերը
    board.white_tray = [Piece("white") for _ in range(15)]
    board.black_tray = [Piece("black") for _ in range(15)]

    # Տախտակը դատարկ ենք թողնում
    for point in board.points:
        point.stack.clear()

def start_long_game():
    global board
    board = Board()
    board.white_tray = [Piece("white") for _ in range(15)]
    board.black_tray = [Piece("black") for _ in range(15)]
    for point in board.points:
        point.stack.clear()

def get_enter_step(end_index, color):
    if color == "white":
        return 24 - end_index
    else:
        return end_index + 1

#ստուգելու արդյոք խաղացողը ունի tray քարեր
def player_has_bar(color):
    if color == "white":
        return len(board.white_tray) > 0
    else:
        return len(board.black_tray) > 0
    
def can_bear_off(start_index, step, color):
    """
    Ստուգում է՝ կարո՞ղ է քարը դուրս բերվել խաղից:
    """
    # ---- Սպիտակ ----
    if color == "white":
        home = range(18, 24)

        # Բոլոր 15 քարերը պիտի home լինեն
        for p in range(0,18):
            if any(piece.color=="white" for piece in board.points[p].stack):
                return False

        end_index = start_index + step
        return end_index >= 24

    # ---- Սև ----
    else:
        home = range(0,6)

        for p in range(6,24):
            if any(piece.color=="black" for piece in board.points[p].stack):
                return False

        end_index = start_index - step
        return end_index < 0
    

def get_valid_moves(start_index, color):
    global current_steps
    if not dice_ready:
        return []

    moves = []

    # tray / bar
    if player_has_bar(color):
        enter_range = range(18, 24) if color=="white" else range(0,6)
        for step in current_steps:
            end_index = 24 - step if color=="white" else step - 1
            if end_index in enter_range:
                target = board.points[end_index].stack
                if len(target) <= 1 or target[-1].color == color:
                    moves.append(end_index)
        return moves

    # սովորական moves
    for step in current_steps:
        end_index = start_index + step if color=="white" else start_index - step
        if 0 <= end_index < 24:
            target = board.points[end_index].stack
            if len(target) == 0 or target[-1].color == color or len(target) == 1:
                moves.append(end_index)
        else:
            if can_bear_off(start_index, step, color):
                moves.append("BEAR")
    return moves

def move_piece(start_index, end, piece):
    global current_steps, white_turn

    color = piece.color

    # ---- BEARING OFF ----
    if end == "BEAR":
        step = max(current_steps)
        current_steps.remove(step)
        board.points[start_index].stack.pop()
        return True

    # ---- STEP CONSUMPTION ----
    step = abs(end - start_index)
    if step in current_steps:
        current_steps.remove(step)
    else:
        bigger_steps = [s for s in current_steps if s > step]
        if bigger_steps:
            current_steps.remove(min(bigger_steps))

    # ---- HITTING ----
    target = board.points[end].stack
    if len(target) == 1 and target[-1].color != color:
        beaten = target.pop()
        # հանգիստ պահենք tray-ում և մաքրենք animation դիրքը
        beaten.in_tray = True
        beaten.animation_pos = None
        if beaten.color == "white":
            board.white_tray.append(beaten)
        else:
            board.black_tray.append(beaten)

    # ---- NORMAL MOVE ----
    board.points[start_index].stack.pop()
    board.points[end].stack.append(piece)

    return True

white_animation_queue = []
black_animation_queue = []
current_color_turn = "white"
piece_animation_queue = []
def animate_pieces_to_positions():
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

        # Սևեր → tray վերևից դեպի ներքև
        if color == "black":
            start_y = tray_rect.top + radius
            def get_y(i): return start_y + i * overlap

        # Սպիտակներ → tray ներքևից դեպի վերև
        else:
            start_y = tray_rect.bottom - radius
            def get_y(i): return start_y - i * overlap

        for i in range(count):
            if len(tray) == 0:
                break

            piece = tray.pop()
            piece.in_tray = False

            # Սկզբնական դիրքը tray-ում՝ ըստ ուղղության
            start_pos = pygame.Vector2(x, get_y(i))
            piece.animation_pos = pygame.Vector2(start_pos)

            end_pos = pygame.Vector2(board_point_to_pixel(pos_index, 0))

            item = {
                "piece": piece,
                "start": start_pos,
                "end": end_pos,
                "end_index": pos_index,
                "t": 0.0
            }

            if color == "white":
                white_animation_queue.append(item)
            else:
                black_animation_queue.append(item)

def update_animation(dt):
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
            board.points[item["end_index"]].add(piece)
            queue.pop(0)
            continue
        ease_t = -0.5*math.cos(math.pi*t)+0.5
        piece.animation_pos = start.lerp(end, ease_t)
        piece.animation_pos.y -= math.sin(math.pi*ease_t)*arc_height
        item["t"] = t

def board_point_to_pixel(index, stack_index):
    radius = 17   
    spacing = 2   # քարի միջանկյալ տարածություն

    if index < 12:  # վերին հատված
        x = BOARD_X + index * triangle_width + triangle_width / 2
        y = BOARD_Y + radius + stack_index * (2 * radius + spacing)
    else:  # ներքևի հատված
        rev = 23 - index
        x = BOARD_X + rev * triangle_width + triangle_width / 2
        y = BOARD_Y + BOARD_HEIGHT - radius - stack_index * (2 * radius + spacing)
    
    return (x, y)


game_started = False
selected_piece = None
selected_index = None
valid_moves = []
dice_ready = False
white_turn = True
current_steps = []
running = True

# ==========================
# Main loop
# ==========================
while running:
    dt = clock.tick(FPS) / 16

    for event in pygame.event.get():

        # ------------------------------------------------------------
        #                        EXIT
        # ------------------------------------------------------------
        if event.type == pygame.QUIT:
            running = False

        # ============================================================
        #                    MOUSE BUTTON DOWN
        # ============================================================
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # --- Short game ---
            if short_button.collidepoint(event.pos):
                start_short_game()
                animate_pieces_to_positions()
                game_started = True
                selected_piece = None
                selected_index = None
                valid_moves = []
                dice_ready = False
                roll_dice_for_turn()
                continue

            # --- Long game ---
            if long_button.collidepoint(event.pos):
                start_long_game()
                animate_pieces_to_positions()
                game_started = True
                selected_piece = None
                selected_index = None
                valid_moves = []
                dice_ready = False
                roll_dice_for_turn()
                continue

            if not game_started:
                continue

            # =====================================================
            #               Tray / Bar Priority Logic
            # =====================================================
            if dice_ready:
                color = "white" if white_turn else "black"
                point_index = get_point_index(mx, my)

                # Tray logic
                if player_has_bar(color):
                    tray = board.white_tray if color == "white" else board.black_tray
                    piece = tray[-1]
                    valid_moves = get_valid_moves(None, color) or []

                    if point_index in valid_moves:
                        tray.pop()
                        piece.in_tray = False
                        piece.animation_pos = None
                        board.points[point_index].stack.append(piece)

                        used_step = get_enter_step(point_index, color)
                        if used_step in current_steps:
                            current_steps.remove(used_step)

                        if not current_steps:
                            dice_ready = False
                            change_turn()

                    continue

                # =====================================================
                #             Normal piece selection
                # =====================================================
                if selected_piece is None:
                    point_index = get_point_index(mx, my)
                    if point_index is not None:
                        stack = board.points[point_index].stack
                        if stack and stack[-1].color == color:
                            piece = stack[-1]
                            px, py = board_point_to_pixel(point_index, len(stack)-1)
                            if (mx - px)**2 + (my - py)**2 <= 17**2:
                                piece.dragging = True
                                piece.drag_offset = (px - mx, py - my)
                                selected_piece = piece
                                selected_index = point_index
                                valid_moves = get_valid_moves(point_index, piece.color) or []

                # =====================================================
                #             Move piece (mouse click)
                # =====================================================
                else:
                    point_index = get_point_index(mx, my)
                    valid_moves = valid_moves or []

                    if point_index in valid_moves or "BEAR" in valid_moves:
                        end = point_index if point_index in valid_moves else "BEAR"

                        move_piece(selected_index, end, selected_piece)

                        selected_piece.is_selected = False
                        selected_piece.dragging = False
                        selected_piece = None
                        selected_index = None
                        valid_moves = []

                        # Step-ները հանվում են move_piece-ի մեջ
                        if not current_steps:
                            dice_ready = False
                            change_turn()

                    else:
                        # Reselection
                        if point_index is not None:
                            stack = board.points[point_index].stack
                            if stack and stack[-1].color == color:
                                selected_piece.is_selected = False
                                selected_piece = stack[-1]
                                selected_index = point_index
                                selected_piece.is_selected = True
                                valid_moves = get_valid_moves(point_index, color) or []
                        else:
                            selected_piece.is_selected = False
                            selected_piece = None
                            selected_index = None
                            valid_moves = []

        # ============================================================
        #                    MOUSE MOTION (dragging)
        # ============================================================
        elif event.type == pygame.MOUSEMOTION:
            if selected_piece and selected_piece.dragging:
                mx, my = event.pos
                ox, oy = selected_piece.drag_offset
                selected_piece.animation_pos = pygame.Vector2(mx + ox, my + oy)

        # ============================================================
        #                    MOUSE BUTTON UP (drop piece)
        # ============================================================
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece and selected_piece.dragging:
                selected_piece.dragging = False
                drop_point = get_point_index(*event.pos)
                color = selected_piece.color

                if drop_point in valid_moves or "BEAR" in valid_moves:
                    end = drop_point if drop_point in valid_moves else "BEAR"

                    # Քարը stack-ից հանենք միայն երբ լեգալ է
                    if selected_index is not None and end != "BEAR":
                        board.points[selected_index].stack.pop()
                    if end != "BEAR":
                        board.points[end].stack.append(selected_piece)
                        px, py = board_point_to_pixel(end, len(board.points[end].stack)-1)
                        selected_piece.animation_pos = pygame.Vector2(px, py)
                    else:
                        selected_piece.in_tray = True
                        selected_piece.animation_pos = None

                    # Step թարմացում
                    used_step = get_enter_step(end if end != "BEAR" else selected_index, color)
                    if used_step in current_steps:
                        current_steps.remove(used_step)

                    # Տուռի ավարտը ստուգում
                    if not current_steps:
                        dice_ready = False
                        change_turn()

                else:
                    # Անօրինական շարժում → վերադարձնել սկզբնական դիրք
                    if selected_index is not None:
                        stack = board.points[selected_index].stack
                        px, py = board_point_to_pixel(selected_index, len(stack)-1)
                        selected_piece.animation_pos = pygame.Vector2(px, py)
                    else:
                        selected_piece.animation_pos = None

                selected_piece = None
                selected_index = None
                valid_moves = []

        # ============================================================
        #                        KEY PRESS
        # ============================================================
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_started:
                animate_pieces_to_positions()
                continue

    # ------------------------------------------------------------
    #                Update animations + dice
    # ------------------------------------------------------------
    update_animation(dt)

    screen.fill(BG_COLOR if game_started else (50, 50, 80))

    if not game_started:
        draw_buttons()
    else:
        draw_board()
        draw_trays_and_pieces(screen, board)
        draw_all_pieces()
        draw_buttons()

        # Հիմնական փոփոխություն այստեղ
        for dice in dice_list:
            dice.update(dt)
            dice.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()