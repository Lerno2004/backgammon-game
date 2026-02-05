def compute_steps(dice_list):
    d1 = dice_list[0].value
    d2 = dice_list[1].value

    if d1 == d2:
        return [d1] * 4
    else:
        return [d1, d2]