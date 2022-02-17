import pygame

from game.config import Config
from game.const import Color, Const
from game.game_state import GameState
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

        self.blue_square_surf = pygame.Surface(
            (Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT)
        )
        self.blue_square_surf.fill(Color.BLUE)

        WALL_LENGTH = 1000
        self.v_wall_surf = pygame.Surface(
            (Const.PLAYER_WIDTH, WALL_LENGTH)
        )
        self.v_wall_surf.fill(Color.WHITE)
        self.h_wall_surf = pygame.Surface(
            (WALL_LENGTH, Const.PLAYER_HEIGHT)
        )
        self.h_wall_surf.fill(Color.WHITE)

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

    def update(self):
        game_state = GameState.get_instance()

        self.screen.fill(Color.BLACK)

        WALL_LENGTH = 1000  # pixels
        for h_wall in (game_state.walls[key] for key in ("top", "bot")):
            self._blit(self.h_wall_surf, h_wall, (WALL_LENGTH, Const.PLAYER_HEIGHT))
        for v_wall in (game_state.walls[key] for key in ("left", "right")):
            self._blit(self.v_wall_surf, v_wall, (Const.PLAYER_HEIGHT, WALL_LENGTH))

        self._blit(self.blue_square_surf, (0, 0), (Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT))