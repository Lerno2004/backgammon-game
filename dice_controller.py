#Հերթ փոխել + զար գցել
import pygame

def change_turn(state, dice_list):
    state["white_turn"] = not state["white_turn"]
    state["current_steps"].clear()
    state["dice_ready"] = False

    for d in dice_list:
        d.value = None
        d.is_rolling = False
        d.roll_time = 0

    roll_dice_for_turn(dice_list, state["white_turn"])


def roll_dice_for_turn(dice_list, white_turn):
    start_x = 212 if white_turn else 567
    y = 350

    for i, dice in enumerate(dice_list):
        dice.target = pygame.Vector2(start_x + i * 100, y)
        dice.roll(white_turn)