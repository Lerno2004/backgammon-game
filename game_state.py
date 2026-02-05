from dice import Dice
from piece import Board
current_steps = []     # [3,6] կամ [4,4,4,4]
dice_ready = False
must_enter = False
game_over = False
board = Board()       # Տախտակը
white_turn = True     # Տուրի տիրույթ
dice_ready = False    # Զարերը պատրաստ են
current_steps = []    # Կա քայլերի ցուցակ
white_turn = True
state = {
    "white_turn": True,
    "dice_ready": False,
    "current_steps": []
}
