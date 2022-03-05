import pygame

from blue_square.const import Color, Const
from blue_square.game_state import BlueSquareGameState
from game.window import Window as GameWindow


class Window(GameWindow):
    def __init__(self):
        super().__init__()

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

    def update(self):
        game_state = BlueSquareGameState.get_instance()

        self.screen.fill(Color.BLACK)

        WALL_LENGTH = 1000  # pixels
        for h_wall in (game_state.walls[key] for key in ("top", "bot")):
            pos = (
                h_wall[0] - game_state.blue_square_pos[0],
                h_wall[1] - game_state.blue_square_pos[1],
            )
            self._blit(self.h_wall_surf, pos, (WALL_LENGTH, Const.PLAYER_HEIGHT))
        for v_wall in (game_state.walls[key] for key in ("left", "right")):
            pos = (
                v_wall[0] - game_state.blue_square_pos[0],
                v_wall[1] - game_state.blue_square_pos[1],
            )
            self._blit(self.v_wall_surf, pos, (Const.PLAYER_HEIGHT, WALL_LENGTH))

        self._blit(self.blue_square_surf, (0, 0), (Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT))
