import threading
import time

import pygame

from game.const import Const
from game.window import Window
from game.game_state import GameState
from game.exceptions import Quit

_DEFAULT = None


def main(_window=_DEFAULT, _game_state=_DEFAULT):
    pygame.init()

    window = _window or Window.get_instance()
    game_state = _game_state or GameState.get_instance()

    while True:
        sleeper = threading.Thread(
            target=time.sleep,
            args=(Const.STEP_DURATION,)
        )
        sleeper.start()

        try:
            game_state.update()
        except Quit:
            return

        window.update()

        sleeper.join()
        pygame.display.flip()


if __name__ == "__main__":
    main()
