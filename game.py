from cmath import sqrt
import json
import logging
import pathlib
import threading
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
    FRAME_RATE = 120  # frames per sec
    PLAYER_WIDTH = 30  # pixels
    PLAYER_HEIGHT = 30  # pixels
    PLAYER_STEP_PPS = 600  # pixels per sec
    PLAYER_SPRINT_PPS = 1200  # pixels per sec

    STEP_DURATION = round(1 / FRAME_RATE * 1000) / 1000
    PLAYER_STEP = round(PLAYER_STEP_PPS / FRAME_RATE)
    PLAYER_SPRINT = round(PLAYER_SPRINT_PPS / FRAME_RATE)


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

        self.blue_square = pygame.Surface(
            (Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT)
        )
        WALL_LENGTH = 1000
        self.blue_square.fill(Color.BLUE)
        self.v_wall_surf = pygame.Surface(
            (Const.PLAYER_WIDTH, WALL_LENGTH)
        )
        self.v_wall_surf.fill(Color.WHITE)
        self.h_wall_surf = pygame.Surface(
            (WALL_LENGTH, Const.PLAYER_HEIGHT)
        )
        self.h_wall_surf.fill(Color.WHITE)

    def update(self):
        screen = self.screen
        w = screen.get_width()
        h = screen.get_height()
        ow, oh = (w // 2, h // 2)
        game_state = GameState.get_instance()

        screen.fill(Color.BLACK)
        screen.blit(self.blue_square, (
            (w - Const.PLAYER_WIDTH) // 2,
            (h - Const.PLAYER_HEIGHT) // 2
        ))
        WALL_LENGTH = 1000  # pixels

        for h_wall in (game_state.walls[key] for key in ("top", "bot")):
            screen.blit(self.h_wall_surf, (
                ow + h_wall[0] - game_state.blue_square_pos[0] - WALL_LENGTH // 2,  # noqa E501
                oh + h_wall[1] - game_state.blue_square_pos[1] - Const.PLAYER_HEIGHT // 2,  # noqa E501
            ))
        for v_wall in (game_state.walls[key] for key in ("left", "right")):
            screen.blit(self.v_wall_surf, (
                ow + v_wall[0] - game_state.blue_square_pos[0] - Const.PLAYER_WIDTH // 2,  # noqa E501
                oh + v_wall[1] - game_state.blue_square_pos[1] - WALL_LENGTH // 2,  # noqa E501
            ))


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
    window = GlobalWindow.get_instance()
    game_state = GameState.get_instance()

    while True:
        sleeper = threading.Thread(
            target=lambda: time.sleep(Const.STEP_DURATION)
        )
        sleeper.start()

        try:
            game_state.update()
        except Quit:
            return

        window.update()

        sleeper.join()
        pygame.display.flip()


pygame.init()
loop()
