import pygame
from settings import *
from piece import Piece
white_piece_surface = pygame.image.load("white_piece.png").convert_alpha()
white_piece_surface = pygame.transform.smoothscale(white_piece_surface, (40, 40))
black_piece_surface = pygame.image.load("black_piece.png").convert_alpha()
black_piece_surface = pygame.transform.smoothscale(black_piece_surface, (40, 40))

def draw_frame(screen, rect):
    FRAME_COLOR = (54, 37, 25)
    LIGHT_EDGE  = (102, 76, 52)
    DARK_EDGE   = (79, 58, 40)

    frame_rect = pygame.Rect(
        rect.x - 15,
        rect.y - 15,
        rect.width + 30,
        rect.height + 30
    )

    pygame.draw.rect(screen, FRAME_COLOR, frame_rect)

    pygame.draw.line(screen, LIGHT_EDGE, frame_rect.topleft, frame_rect.topright, 3)
    pygame.draw.line(screen, LIGHT_EDGE, frame_rect.topleft, frame_rect.bottomleft, 3)
    pygame.draw.line(screen, DARK_EDGE, frame_rect.bottomleft, frame_rect.bottomright, 3)
    pygame.draw.line(screen, DARK_EDGE, frame_rect.topright, frame_rect.bottomright, 3)

def draw_board(SCREEN, wood_texture, board_texture):
    # Փայտե ֆոն
    SCREEN.blit(wood_texture, (0, 0))

    # Շրջանակ
    FRAME_COLOR = (54, 37, 25)
    frame_rect = pygame.Rect(
        BOARD_X - 15, BOARD_Y - 15,
        BOARD_WIDTH + 30, BOARD_HEIGHT + 30
    )
    pygame.draw.rect(SCREEN, FRAME_COLOR, frame_rect)

    LIGHT_EDGE  = (102, 76, 52)
    DARK_EDGE   = (79, 58, 40)

    pygame.draw.line(SCREEN, LIGHT_EDGE, frame_rect.topleft, frame_rect.topright, 3)
    pygame.draw.line(SCREEN, LIGHT_EDGE, frame_rect.topleft, frame_rect.bottomleft, 3)
    pygame.draw.line(SCREEN, DARK_EDGE, frame_rect.bottomleft, frame_rect.bottomright, 3)
    pygame.draw.line(SCREEN, DARK_EDGE, frame_rect.topright, frame_rect.bottomright, 3)

    # ✅ Պատրաստի տախտակի texture
    SCREEN.blit(board_texture, (BOARD_X, BOARD_Y))
    

def draw_piece(screen, x, y, piece):
    radius = 20
    if piece.animation_pos is not None:
        x, y = piece.animation_pos

    # օգտագործել պատրաստի surface, առանց նորից բեռնելու
    surf = white_piece_surface if piece.color == "white" else black_piece_surface
    screen.blit(surf, (x - radius, y - radius))

def get_point_index(mx, my):
    """Վերադարձնել տախտակի կետի index-ը մկնիկի դիրքից"""
    if not (BOARD_X <= mx <= BOARD_X + BOARD_WIDTH):
        return None
    if not (BOARD_Y <= my <= BOARD_Y + BOARD_HEIGHT):
        return None

    local_x = mx - BOARD_X
    triangle = int(local_x // TRIANGLE_WIDTH)

    if my < BOARD_Y + BOARD_HEIGHT // 2:
        return triangle
    else:
        return 23 - triangle
    
def draw_buttons(screen):
    """Նկարել Կարճ և Երկար խաղ կոճակները"""
    pygame.draw.rect(screen, (40, 40, 40), SHORT_BUTTON, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), LONG_BUTTON, border_radius=8)

    font_name = "NotoSansArmenian-VariableFont_wdth,wght.ttf"
    
    def render_text_fit(button, text):
        font_size = 32
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

    short_text_surf, short_text_rect = render_text_fit(SHORT_BUTTON, "Կարճ խաղ")
    long_text_surf, long_text_rect   = render_text_fit(LONG_BUTTON, "Երկար խաղ")

    screen.blit(short_text_surf, short_text_rect)
    screen.blit(long_text_surf, long_text_rect)


    SCREEN.blit(short_text_surf, short_text_rect)
    SCREEN.blit(long_text_surf, long_text_rect)

def draw_right_trays(screen):
    # White tray frame
    draw_frame(screen, RIGHT_TRAY_WHITE)

    # Black tray frame
    draw_frame(screen, RIGHT_TRAY_BLACK)

def draw_pieces_in_tray(screen, pieces, tray_rect):
    """Նկարել քարերը տրեյում"""
    piece_radius = 17
    overlap = piece_radius
    x = tray_rect.centerx
    start_y = tray_rect.top + piece_radius

    for i, piece in enumerate(reversed(pieces)):
        y = start_y + i * overlap
        if getattr(piece, "animation_pos", None) is not None:
            px, py = int(piece.animation_pos.x), int(piece.animation_pos.y)
            draw_piece(screen, px, py, piece)
        else:
            draw_piece(screen, int(x), int(y), piece)

def draw_all_pieces(screen, board, white_animation_queue, black_animation_queue):
    # Նկարել տախտակի stack-երը
    for point in board.points:
        for i, piece in enumerate(point.stack):
            pos = piece.animation_pos if piece.animation_pos else board_point_to_pixel(point.index, i)
            draw_piece(screen, int(pos[0]), int(pos[1]), piece)
    # Նկարել animation queue-ում եղած քարերը
    for queue in [white_animation_queue, black_animation_queue]:
        for item in queue:
            piece = item["piece"]
            draw_piece(screen, int(piece.animation_pos.x), int(piece.animation_pos.y), piece)
            
def draw_trays_and_pieces(screen, board):
    """Նկարել տրեյերը և դրանց մեջ քարերը"""
    draw_right_trays(screen)
    draw_pieces_in_tray(screen, board.white_tray, RIGHT_TRAY_WHITE)
    draw_pieces_in_tray(screen, board.black_tray, RIGHT_TRAY_BLACK)

def board_point_to_pixel(index, stack_index):
    # Հաստատուն չափեր
    BOARD_X = 132
    BOARD_Y = 82
    BOARD_WIDTH = 656
    BOARD_HEIGHT = 573
    
    # Նկարից դատելով՝ BAR_WIDTH-ը մոտավորապես 40-44 պիքսել է
    BAR_WIDTH = 63
    
    # ԿԱՐԵՎՈՐ: Եռանկյունու լայնությունը՝ առանց Bar-ի
    TRIANGLE_WIDTH = (BOARD_WIDTH - BAR_WIDTH) / 12
    
    radius = 13
    spacing = 6

    # Որոշում ենք կողմը
    # 0-5 (ձախ վերև), 6-11 (աջ վերև)
    # 12-17 (աջ ներքև), 18-23 (ձախ ներքև)
    is_right_side = (6 <= index <= 17)

    if index < 12:  # Վերևի հատված (0-ից 11)
        x = BOARD_X + (index * TRIANGLE_WIDTH) + (TRIANGLE_WIDTH / 2)
        if is_right_side:
            x += BAR_WIDTH
        y = BOARD_Y + radius + stack_index * (2 * radius + spacing)+7
    else:  # Ներքևի հատված (12-ից 23)
        # Շրջում ենք ինդեքսը, որպեսզի 23-ը լինի ձախում, 12-ը՝ աջում
        visual_index = 23 - index 
        x = BOARD_X + (visual_index * TRIANGLE_WIDTH) + (TRIANGLE_WIDTH / 2)
        if is_right_side:
            x += BAR_WIDTH
        y = BOARD_Y + BOARD_HEIGHT - radius - stack_index * (2 * radius + spacing)-1
    
    return (int(x), int(y))