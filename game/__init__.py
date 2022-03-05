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


def main(_config=_DEFAULT, _window=_DEFAULT, _game_state=_DEFAULT):
    pygame.init()
    context = ContextManager.init_singleton(_config, _window, _game_state)

    window = context.window
    game_state = context.game_state

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
