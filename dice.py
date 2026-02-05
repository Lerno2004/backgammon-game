import pygame
import random
from dice_logic import compute_steps
from settings import *

class Dice:
    def __init__(self, start_pos):
        self.pos = pygame.Vector2(start_pos)
        self.target = pygame.Vector2(start_pos)
        self.value = None
        self.roll_time = 0
        self.is_rolling = False
        self.velocity = pygame.Vector2(0, 0)

    def roll(self, white_turn):
        self.is_rolling = True
        self.value = None
        x_vel = -random.uniform(6, 12) if white_turn else random.uniform(6, 12)
        y_vel = -random.uniform(10, 15)
        self.velocity = pygame.Vector2(x_vel, y_vel)

    def update(self, dt, state, dice_list):
        if self.is_rolling:
            self.roll_time += dt
            self.velocity.y += 0.5
            self.pos += self.velocity

            # ✅ Clamp զարի դիրքը՝ տախտակի ներսում
            self.pos.x = max(BOARD_X, min(self.pos.x, BOARD_X + BOARD_WIDTH - DICE_SIZE))
            self.pos.y = max(BOARD_Y, min(self.pos.y, BOARD_Y + BOARD_HEIGHT - DICE_SIZE))

            if self.pos.y >= self.target.y:
                self.pos.y = self.target.y
                self.velocity.y *= -0.3

                if abs(self.velocity.y) < 1:
                    self.is_rolling = False
                    self.velocity = pygame.Vector2(0, 0)
                    self.value = random.randint(1,6)

        else:
            # Երբ ոչ rolling, զարը թեքվում է target-ի կողմը
            self.pos += (self.target - self.pos) * 0.1

            # Clamp այստեղ ևս, որ ավտոմատ շարժման ժամանակ չհեռանա
            self.pos.x = max(BOARD_X, min(self.pos.x, BOARD_X + BOARD_WIDTH - DICE_SIZE))
            self.pos.y = max(BOARD_Y, min(self.pos.y, BOARD_Y + BOARD_HEIGHT - DICE_SIZE))

        # Ստուգում՝ բոլորը կանգնած են → հաշվարկել steps
        if (
            not state["dice_ready"]
            and all(not d.is_rolling for d in dice_list)
            and all(d.value is not None for d in dice_list)
        ):
            state["current_steps"] = compute_steps(dice_list)
            state["dice_ready"] = True          

    def draw(self, screen, dice_textures):
        if self.is_rolling:
            v = random.randint(1, 6)
            screen.blit(dice_textures[v - 1], self.pos)
        elif self.value is not None:
            screen.blit(dice_textures[self.value - 1], self.pos)
