from enum import auto

from pygame import K_DOWN, K_LEFT, K_LSHIFT, K_RIGHT, K_UP, K_a, K_d, K_q, K_s, K_w, K_z

from game import Controls as GameControls


class Controls(GameControls):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    SPRINT = auto()

    def __init__(self, config):
        super().__init__(config)
        self.keymap.update({
            Controls.LEFT: [K_LEFT, K_q, K_a],
            Controls.RIGHT: [K_RIGHT, K_d],
            Controls.UP: [K_UP, K_z, K_w],
            Controls.DOWN: [K_DOWN, K_s],
            Controls.SPRINT: [K_LSHIFT],
        })
