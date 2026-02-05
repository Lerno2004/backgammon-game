#Բոլոր նկարների բեռնումը
import pygame
from settings import *

def load_assets():
    wood_texture = pygame.image.load(
        "/Users/lernikpetrosyan/Desktop/Brown Wood Texture_276_2048.jpg"
    ).convert()
    wood_texture = pygame.transform.scale(wood_texture, (WIDTH, HEIGHT))

    board_texture = pygame.image.load(
        "/Users/lernikpetrosyan/Desktop/Birch Wood Texture_285_2048 2.jpg"
    ).convert()
    board_texture = pygame.transform.scale(
        board_texture, (BOARD_WIDTH, BOARD_HEIGHT)
    )

    triangle_texture = pygame.image.load(
        "/Users/lernikpetrosyan/Desktop/walnut-wood-texture-.jpg"
    ).convert()
    triangle_texture = pygame.transform.scale(
        triangle_texture,
        (int(TRIANGLE_WIDTH), int(TRIANGLE_HEIGHT))
    )

    frame_texture = pygame.transform.scale(
        triangle_texture, (BOARD_WIDTH + 30, BOARD_HEIGHT + 30)
    )

    # Dice textures
    dice_textures = []
    for i in range(1, 7):
        img = pygame.image.load(
            f"/Users/lernikpetrosyan/Desktop/dice_faces_hd/{i}_dots.png"
        ).convert_alpha()
        img = pygame.transform.scale(img, (DICE_SIZE, DICE_SIZE))
        dice_textures.append(img)

    return {
        "wood": wood_texture,
        "board": board_texture,
        "triangle": triangle_texture,
        "frame": frame_texture,
        "dice": dice_textures
    }