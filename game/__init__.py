import threading
import time

import pygame

from game.config import Config
from game.const import Const
from game.context_manager import ContextManager
from game.controls import Controls
from game.exceptions import Quit
from game.game_state import GameState
from game.window import Window

_DEFAULT = None


def main(_config=_DEFAULT, _controls=_DEFAULT, _window=_DEFAULT, _game_state=_DEFAULT):
    pygame.init()
    config = _config() if _config else Config()
    config.load()

    controls = _controls(config) if _controls else Controls(config)
    window = _window(config) if _window else Window(config)
    game_state = _game_state() if _game_state else GameState()

    ContextManager.init_singleton(config, controls, window, game_state)

    while True:
        sleeper = threading.Thread(
            target=time.sleep,
            args=(Const.STEP_DURATION,)
        )
        sleeper.start()

        pygame.event.pump()
        try:
            controls.update()
            game_state.update()
        except Quit:
            game_state.on_exit()
            return

        window.update()

        sleeper.join()
        pygame.display.flip()
