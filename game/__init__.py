import threading
import time

import pygame

from game.config import Config
from game.const import Const
from game.controls import Controls
from game.exceptions import Quit
from game.game_state import GameState
from game.window import Window

_DEFAULT = None


def main(_config=_DEFAULT, _window=_DEFAULT, _game_state=_DEFAULT):
    pygame.init()

    config = _config or Config.get_instance()
    config.load()
    window = _window or Window.get_instance()
    game_state = _game_state or GameState.get_instance()

    while True:
        sleeper = threading.Thread(
            target=time.sleep,
            args=(Const.STEP_DURATION,)
        )
        sleeper.start()

        pygame.event.pump()
        try:
            game_state.update()
        except Quit:
            game_state.on_exit()
            return

        window.update()

        sleeper.join()
        pygame.display.flip()
