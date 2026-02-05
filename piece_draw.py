import pygame

def draw_piece(screen, x, y, piece):
    radius = 17

    if piece.animation_pos is not None:
        x, y = piece.animation_pos

    shadow = (204, 189, 182, 110) if piece.color == "white" else (0, 0, 0, 180)
    pygame.draw.circle(screen, shadow, (x + 3, y + 3), radius)

    surf = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)

    base = (240, 230, 220) if piece.color == "white" else (60, 40, 30)
    pygame.draw.circle(surf, base, (radius + 2, radius + 2), radius)

    border = (179, 161, 139) if piece.color == "white" else (40, 20, 10)
    pygame.draw.circle(surf, border, (radius + 2, radius + 2), radius, 2)

    if piece.is_selected:
        pygame.draw.circle(surf, (0, 255, 0), (radius + 2, radius + 2), radius + 2, 3)

    screen.blit(surf, (x - radius - 2, y - radius - 2))