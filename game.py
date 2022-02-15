from cmath import sqrt
import json
import logging
import pathlib
import time

import pygame


class Singleton:
    _singleton = None

    @classmethod
    def get_instance(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton


class Const:
    STEP_DURATION = 0.010
    PLAYER_WIDTH = 30
    PLAYER_HEIGHT = 30
    PLAYER_STEP = 5
    PLAYER_SPRINT = 10
    WALL_LENGTH = 1000


class Color:
    BLACK = 0x000000
    WHITE = 0XFFFFFF
    BLUE = 0x0000FF


class Config(Singleton):
    _FILE = "gameconfig"

    def __init__(self):
        self.HEIGHT = 1080
        self.WIDTH = self.HEIGHT * 16 // 9
        self.FULLSCREEN = False
        self.BORDERLESS = True
        if pathlib.Path(Config._FILE).is_file():
            with open(Config._FILE) as f:
                try:
                    self.__dict__.update(json.load(f))
                except json.JSONDecodeError as e:
                    logging.error(
                        f"Failed to read config file '{Config._FILE}': "
                        f"{e}"
                    )

    def save(self):
        with open(Config._FILE, 'w') as f:
            json.dump(self.__dict__, f)


class GlobalWindow(Singleton):
    _singleton = None

    def __init__(self):
        config = Config.get_instance()
        size = config.WIDTH, config.HEIGHT
        fullscreen = pygame.FULLSCREEN if config.FULLSCREEN else 0
        borderless = pygame.NOFRAME if config.BORDERLESS else 0
        self.screen = pygame.display.set_mode(
            size, fullscreen | borderless
        )


class Quit(Exception):
    pass


HORIZONTAL = pygame.K_LEFT, pygame.K_RIGHT
VERTICAL = pygame.K_UP, pygame.K_DOWN
ORTH = {
    pygame.K_UP: HORIZONTAL, pygame.K_DOWN: HORIZONTAL,
    pygame.K_LEFT: VERTICAL, pygame.K_RIGHT: VERTICAL
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
                sqrt(2).real / 2
                if any(keydown[orth] for orth in ORTH[direction])
                else 1
            )
            return round(step * diagonal_factor)
        self.blue_square_pos[0] += (
            _step_toward(pygame.K_RIGHT) - _step_toward(pygame.K_LEFT)
        )
        self.blue_square_pos[1] += (
            _step_toward(pygame.K_DOWN) - _step_toward(pygame.K_UP)
        )


def loop():
    screen = GlobalWindow.get_instance().screen
    w = screen.get_width()
    h = screen.get_height()
    ow, oh = (w // 2, h // 2)
    gameState = GameState.get_instance()
    blue_square = pygame.Surface((Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT))
    blue_square.fill(Color.BLUE)
    v_wall_surf = pygame.Surface((Const.PLAYER_WIDTH, Const.WALL_LENGTH))
    v_wall_surf.fill(Color.WHITE)
    h_wall_surf = pygame.Surface((Const.WALL_LENGTH, Const.PLAYER_HEIGHT))
    h_wall_surf.fill(Color.WHITE)

    while True:
        try:
            gameState.update()
        except Quit:
            return

        screen.fill(Color.BLACK)
        screen.blit(blue_square, (
            (w - Const.PLAYER_WIDTH) // 2,
            (h - Const.PLAYER_HEIGHT) // 2
        ))
        for h_wall in (gameState.walls[key] for key in ("top", "bot")):
            screen.blit(h_wall_surf, (
                ow + h_wall[0] - gameState.blue_square_pos[0] - Const.WALL_LENGTH // 2,
                oh + h_wall[1] - gameState.blue_square_pos[1] - Const.PLAYER_HEIGHT // 2,
            ))
        for v_wall in (gameState.walls[key] for key in ("left", "right")):
            screen.blit(v_wall_surf, (
                ow + v_wall[0] - gameState.blue_square_pos[0] - Const.PLAYER_WIDTH // 2,
                oh + v_wall[1] - gameState.blue_square_pos[1] - Const.WALL_LENGTH // 2,
            ))

        time.sleep(Const.STEP_DURATION)
        pygame.display.flip()


pygame.init()
loop()