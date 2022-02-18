import json
import logging
import pathlib

from pygame import (
    K_DOWN, K_LEFT, K_LSHIFT, K_RIGHT, K_UP, K_a, K_d, K_q, K_s, K_w, K_z
)

from singleton import Singleton


class Config(Singleton):
    _FILE = "gameconfig"

    def __init__(self):
        self.HEIGHT = 1080
        self.WIDTH = self.HEIGHT * 16 // 9
        self.FULLSCREEN = False
        self.BORDERLESS = True

        self.KEYMAP = {
            "LEFT": [K_LEFT, K_q, K_a],
            "RIGHT": [K_RIGHT, K_d],
            "UP": [K_UP, K_z, K_w],
            "DOWN": [K_DOWN, K_s],
            "SPRINT": [K_LSHIFT],
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