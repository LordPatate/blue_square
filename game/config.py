import json
import logging
import pathlib

from pygame import K_ESCAPE

from game.controls import Controls
from singleton import Singleton


class Config(Singleton):
    _FILE = "gameconfig"

    def __init__(self):
        self.HEIGHT = 1080
        self.WIDTH = self.HEIGHT * 16 // 9
        self.FULLSCREEN = False
        self.BORDERLESS = True

        self.KEYMAP = {
            Controls.QUIT: [K_ESCAPE],
        }

    def load(self):
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
