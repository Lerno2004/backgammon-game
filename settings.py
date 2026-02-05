import pygame
# -----------------------
# Screen & FPS
# -----------------------
WIDTH, HEIGHT = 1000, 800
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# -----------------------
# Board
# -----------------------
BOARD_X = 100
BOARD_Y = 50
BOARD_WIDTH = 717
BOARD_HEIGHT = 639

TRIANGLE_WIDTH = BOARD_WIDTH / 12
TRIANGLE_HEIGHT = BOARD_HEIGHT // 3

# -----------------------
# Colors
# -----------------------
WOOD = (122, 196, 153)
BG_COLOR = (122, 196, 153)
BROWN = (0, 81, 163)
CREAM = (140, 194, 255)
WHITE = (255, 255, 255)
LIGHT_WOOD = (237, 244, 255)
DARK_BROWN = (41, 75, 120)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# -----------------------
# Tray / Bar
# -----------------------
TRAY_WIDTH = 10
TRAY_SPACING = 33.5

RIGHT_TRAY_WHITE = pygame.Rect(
    BOARD_X + BOARD_WIDTH + TRAY_SPACING,
    BOARD_Y,
    TRAY_WIDTH,
    BOARD_HEIGHT // 2 - TRAY_SPACING // 2
)

RIGHT_TRAY_BLACK = pygame.Rect(
    BOARD_X + BOARD_WIDTH + TRAY_SPACING,
    BOARD_Y + BOARD_HEIGHT // 2 + TRAY_SPACING // 2,
    TRAY_WIDTH,
    BOARD_HEIGHT // 2 - TRAY_SPACING // 2
)

# -----------------------
# Buttons
# -----------------------
SHORT_BUTTON = pygame.Rect(420, 10, 160, 40)
LONG_BUTTON  = pygame.Rect(600, 10, 160, 40)

# -----------------------
# Dice
# -----------------------
DICE_SIZE = 36   # px
DICE_LIST = []   # Պատրաստել main-ում actual Dice օբյեկտները

# -----------------------
# Animation queues
# -----------------------
white_animation_queue = []
black_animation_queue = []
piece_animation_queue = []

# -----------------------
# Clock / Font
# -----------------------
