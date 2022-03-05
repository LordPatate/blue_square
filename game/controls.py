from collections import defaultdict
from enum import auto

import pygame
from pygame import K_ESCAPE


class Controls:
    QUIT = auto()

    def __init__(self, config):
        self.keydown = defaultdict(lambda: False)
        self.keymap = {
            Controls.QUIT: [K_ESCAPE],
        }
        self.keymap.update(config.KEYMAP)

    def update(self):
        self.keydown = pygame.key.get_pressed()

    def is_pressed(self, control):
        return any(self.keydown[key] for key in self.keymap[control])
