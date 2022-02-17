from math import sqrt

import pygame

from game.const import Const
from game.exceptions import Quit
from singleton import Singleton

HORIZONTAL = pygame.K_LEFT, pygame.K_RIGHT
VERTICAL = pygame.K_UP, pygame.K_DOWN
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
        _ = pygame.event.get()
        keydown = pygame.key.get_pressed()

        if keydown[pygame.K_ESCAPE]:
            raise Quit

        def _step_toward(direction):
            if not keydown[direction]:
                return 0
            step = (
                Const.PLAYER_SPRINT
                if keydown[pygame.K_LSHIFT]
                else Const.PLAYER_STEP
            )
            diagonal_factor = (
                sqrt(2) / 2
                if any(keydown[orth] for orth in ORTH[direction])
                else 1
            )
            return round(step * diagonal_factor)
        self.blue_square_pos[0] += (_step_toward(pygame.K_RIGHT)
                                    - _step_toward(pygame.K_LEFT))
        self.blue_square_pos[1] += (_step_toward(pygame.K_DOWN)
                                    - _step_toward(pygame.K_UP))