import pygame

from game import Config
from singleton import Singleton


class Window(Singleton):
    def __init__(self):
        config = Config.get_instance()
        size = config.WIDTH, config.HEIGHT
        fullscreen = pygame.FULLSCREEN if config.FULLSCREEN else 0
        borderless = pygame.NOFRAME if config.BORDERLESS else 0
        self.screen = pygame.display.set_mode(
            size, fullscreen | borderless
        )

    def update(self):
        pass

    def _blit(self, surface, pos, dim):
        x, y = pos
        w, h = dim
        screen = self.screen
        ox, oy = (screen.get_width() // 2, screen.get_height() // 2)

        screen.blit(
            surface,
            (
                ox + x - (w // 2),
                oy + y - (h // 2),
            )
        )
