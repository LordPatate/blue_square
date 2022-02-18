class Const:
    FRAME_RATE = 120  # frames per sec
    PLAYER_WIDTH = 30  # pixels
    PLAYER_HEIGHT = 30  # pixels
    PLAYER_NORMAL_SPEED = 600  # pixels per sec
    PLAYER_SPRINT_SPEED = 1200  # pixels per sec

    STEP_DURATION = round(1 / FRAME_RATE * 1000) / 1000
    PLAYER_STEP = round(PLAYER_NORMAL_SPEED / FRAME_RATE)
    PLAYER_SPRINT = round(PLAYER_SPRINT_SPEED / FRAME_RATE)


class Color:
    BLACK = 0x000000
    WHITE = 0XFFFFFF
    BLUE = 0x0000FF
