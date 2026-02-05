import pygame, sys
from dice import Dice
from settings import *
from piece import Board
from draw_utils import *
from game_utils import *
from dice_logic import compute_steps
from dice_controller import change_turn, roll_dice_for_turn
from piece_draw import *


pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
wood_texture = pygame.image.load("/Users/lernikpetrosyan/Desktop/Brown Wood Texture_276_2048.jpg").convert()
wood_texture = pygame.transform.scale(wood_texture, (WIDTH, HEIGHT))


board_texture = pygame.image.load("/Users/lernikpetrosyan/Desktop/IMAGE 2026-01-28 16:16:46.jpg").convert()
board_texture = pygame.transform.scale(board_texture, (BOARD_WIDTH, BOARD_HEIGHT))

clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
dice_textures = [pygame.image.load(f"/Users/lernikpetrosyan/Desktop/dice_faces_hd/{i}_dots.png").convert_alpha() for i in range(1,7)]
for i in range(6):
    dice_textures[i] = pygame.transform.scale(dice_textures[i], (DICE_SIZE, DICE_SIZE))


dice_list = [Dice((200, 250)), Dice((300, 250))] # զարերի դիրք տախտակի վրա 
game_started = False
selected_piece = None
selected_index = None
selected_die = None
valid_moves = []
state = {
    "white_turn": True,
    "dice_ready": False,
    "current_steps": []
}
running = True
# Սկզբնական board
board = Board()
# ==========================
# Main loop
# ==========================
while running:
    dt = clock.tick(FPS) / 16

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ============================================================
        # MOUSE BUTTON DOWN
        # ============================================================
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # --- Short game ---
            if SHORT_BUTTON.collidepoint(event.pos):
                board = start_short_game(board)
                animate_pieces_to_positions(board, RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK)
                game_started = True
                state["dice_ready"] = False
                roll_dice_for_turn(dice_list, state["white_turn"])
                continue

            # --- Long game ---
            if LONG_BUTTON.collidepoint(event.pos):
                board = start_long_game(board)
                animate_pieces_to_positions(board, RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK)
                game_started = True
                state["dice_ready"] = False
                roll_dice_for_turn(dice_list, state["white_turn"])
                continue

            if not game_started:
                continue

            # =====================================================
            # Tray / Bar Logic
            # =====================================================
            color = "white" if state["white_turn"] else "black"
            point_index = get_point_index(mx, my)

            if state["dice_ready"] and player_has_bar(board, color):
                tray = board.white_tray if color == "white" else board.black_tray
                piece = tray[-1]
                valid_moves = get_valid_moves(
                                    board,
                                    None,
                                    color,
                                    state
                                )
                if point_index in valid_moves:
                    tray.pop()
                    piece.in_tray = False
                    piece.animation_pos = None
                    board.points[point_index].stack.append(piece)

                    used_step = get_enter_step(point_index, color)
                    if used_step in state["current_steps"]:
                        state["current_steps"].remove(used_step)

                    if not state["current_steps"]:
                        state["dice_ready"] = False
                        change_turn(state, dice_list)

                continue

            # =====================================================
            # Normal piece selection
            # =====================================================
            if selected_piece is None and point_index is not None:
                stack = board.points[point_index].stack
                if stack and stack[-1].color == color:
                    piece = stack[-1]
                    px, py = board_point_to_pixel(point_index, len(stack)-1)
                    if (mx - px)**2 + (my - py)**2 <= 17**2:
                        piece.dragging = True
                        piece.drag_offset = (px - mx, py - my)
                        selected_piece = piece
                        selected_index = point_index
                        valid_moves = get_valid_moves(board, point_index, piece.color, state)

            # =====================================================
            # Move piece click
            # =====================================================
            elif selected_piece is not None:
                # Հիմնական logic՝ քարը տեղադրել
                drop_point = get_point_index(mx, my)
                valid_moves = get_valid_moves(
                            board,
                            selected_index,
                            selected_piece.color,
                            state
                        )
                if drop_point in valid_moves or "BEAR" in valid_moves:
                    end = drop_point if drop_point in valid_moves else "BEAR"

                    # Քարը տեղափոխել եւ current_steps-ը հանել օգտագործված քայլը
                    move_piece(
                            board,
                            selected_index,
                            end,
                            selected_piece,
                            state
                        )
                    # Վերականգնել dragging / selection կարգավիճակը
                    selected_piece.dragging = False
                    selected_piece.is_selected = False
                    selected_piece = None
                    selected_index = None
                    valid_moves = []

                    # Ստուգել steps-երը → հերթ փոխել եթե վերջացել է
                    if not state["current_steps"]:
                        state["dice_ready"] = False
                        change_turn(state, dice_list)

                else:
                    # Եթե չի թույլատրվում → վերականգնել քարի դիրքը animation-ի համար
                    selected_piece.dragging = False
                    selected_piece.is_selected = False
                    if selected_index is not None:
                        stack = board.points[selected_index].stack
                        px, py = board_point_to_pixel(selected_index, len(stack)-1)
                        selected_piece.animation_pos = pygame.Vector2(px, py)
                    else:
                        selected_piece.animation_pos = None

                    selected_piece = None
                    selected_index = None
                    valid_moves = []
        elif event.type == pygame.MOUSEMOTION:
            if selected_piece and selected_piece.dragging:
                mx, my = event.pos
                ox, oy = selected_piece.drag_offset

                new_x = mx + ox
                new_y = my + oy

                radius = 16  # կամ քո քարի իրական radius-ը

                # 🔒 Սահմանափակում՝ տախտակից դուրս չգա
                new_x = max(
                    BOARD_X + radius,
                    min(new_x, BOARD_X + BOARD_WIDTH - radius)
                )
                new_y = max(
                    BOARD_Y + radius,
                    min(new_y, BOARD_Y + BOARD_HEIGHT - radius)
                )

                selected_piece.animation_pos = pygame.Vector2(new_x, new_y)
            elif selected_die and selected_die.dragging:
                mx, my = event.pos
                ox, oy = selected_die.drag_offset

                die_w = selected_die.rect.width
                die_h = selected_die.rect.height

                # Նոր դիրքը՝ հաշվի առնելով drag offset-ը
                new_x = mx + ox
                new_y = my + oy

                # Սահմանափակում՝ ամբողջ զարը մնա տախտակի մեջ
                if new_x < BOARD_X:
                    new_x = BOARD_X
                elif new_x + die_w > BOARD_X + BOARD_WIDTH:
                    new_x = BOARD_X + BOARD_WIDTH - die_w

                if new_y < BOARD_Y:
                    new_y = BOARD_Y
                elif new_y + die_h > BOARD_Y + BOARD_HEIGHT:
                    new_y = BOARD_Y + BOARD_HEIGHT - die_h

                selected_die.rect.topleft = (new_x, new_y)
        # ============================================================
        # MOUSE BUTTON UP
        # ============================================================
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece and selected_piece.dragging:
                selected_piece.dragging = False
                drop_point = get_point_index(*event.pos)

                color = selected_piece.color
                tray = board.white_tray if color == "white" else board.black_tray

                # Եթե bar-ում քար կա → forced move
                if tray:
                    selected_index = None
                    selected_piece = tray[-1]
                    valid_moves = get_valid_moves(board, None, color, state)
                    # drop_point ստուգելու կարիք չկա, քանի որ bar-ից դուրս valid_moves արդեն հաշված է
                    end = valid_moves[0]  # առաջին թույլատրելի քայլը
                    moved = move_piece(board, None, end, selected_piece, state)

                    if moved:
                        px, py = board_point_to_pixel(end, len(board.points[end].stack)-1)
                        selected_piece.animation_pos = pygame.Vector2(px, py)
                        selected_piece = None
                        selected_index = None
                        valid_moves = []

                        if not state["current_steps"]:
                            state["dice_ready"] = False
                            change_turn(state, dice_list)

                else:
                    # Սովորական շարժում
                    if drop_point in valid_moves or "BEAR" in valid_moves:
                        end = drop_point if drop_point in valid_moves else "BEAR"
                        moved = move_piece(board, selected_index, end, selected_piece, state)

                        if moved:
                            if end != "BEAR":
                                px, py = board_point_to_pixel(end, len(board.points[end].stack)-1)
                                selected_piece.animation_pos = pygame.Vector2(px, py)
                            else:
                                selected_piece.animation_pos = None

                            selected_piece = None
                            selected_index = None
                            valid_moves = []

                            if not state["current_steps"]:
                                state["dice_ready"] = False
                                change_turn(state, dice_list)

                    else:
                        # Վերականգնել նախկին դիրքը
                        if selected_index is not None:
                            stack = board.points[selected_index].stack
                            px, py = board_point_to_pixel(selected_index, len(stack)-1)
                            selected_piece.animation_pos = pygame.Vector2(px, py)
                        selected_piece.dragging = False
                        selected_piece = None
                        selected_index = None
                        valid_moves = []
                state["move_done_this_click"] = False

            if event.button == 1 and selected_die:
                selected_die.dragging = False
                selected_die = None
        # ============================================================
        # KEY PRESS
        # ============================================================
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_started:
                animate_pieces_to_positions(board, RIGHT_TRAY_WHITE, RIGHT_TRAY_BLACK)
                continue

    # ============================================================
    # Update animation + dice
    # ============================================================
    update_animation(dt, board)

    SCREEN.fill(BG_COLOR if game_started else (50, 50, 80))
    

    if not game_started:
        draw_buttons(SCREEN)
    else:
        draw_board(SCREEN, wood_texture, board_texture)
        draw_trays_and_pieces(SCREEN, board)
        draw_all_pieces(SCREEN, board, white_animation_queue, black_animation_queue, )
        draw_buttons(SCREEN)

        # --- UPDATE DICE ---
        for dice in dice_list:
            dice.update(dt, state, dice_list)
            

        # --- DRAW DICE ---
        for dice in dice_list:
            dice.draw(SCREEN, dice_textures)
    
    pygame.display.flip()


pygame.quit()
sys.exit()