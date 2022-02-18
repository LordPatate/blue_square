from math import sqrt

import pygame

from game import Config
from game.const import Const
from game.controls import Controls
from game.exceptions import Quit
from singleton import Singleton

HORIZONTAL = Controls.LEFT, Controls.RIGHT
VERTICAL = Controls.UP, Controls.DOWN
ORTH = {
    key: (VERTICAL if key in HORIZONTAL else HORIZONTAL)
    for key in (HORIZONTAL + VERTICAL)
}


class GameState(Singleton):
    def __init__(self):
        self.blue_square_pos = [0, 0]
        self.walls = {
            "top": (0, -400),
            "bot": (0, 400),
            "left": (-400, 0),
            "right": (400, 0),
        }

    def update(self):
        pygame.event.pump()
        keydown = pygame.key.get_pressed()
        config = Config.get_instance()

        def _is_pressed(control):
            return any(keydown[key] for key in config.KEYMAP[control])

        if _is_pressed(Controls.QUIT):
            raise Quit

        def _step_toward(direction):
            if not _is_pressed(direction):
                return 0
            step = (
                Const.PLAYER_SPRINT
                if _is_pressed(Controls.SPRINT)
                else Const.PLAYER_STEP
            )
            diagonal_factor = (
                sqrt(2) / 2
                if any(_is_pressed(orth) for orth in ORTH[direction])
                else 1
            )
            return round(step * diagonal_factor)
        self.blue_square_pos[0] += (_step_toward(Controls.RIGHT)
                                    - _step_toward(Controls.LEFT))
        self.blue_square_pos[1] += (_step_toward(Controls.DOWN)
                                    - _step_toward(Controls.UP))
