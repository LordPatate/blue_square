import game
from singleton import Singleton

_DEFAULT = None


class ContextManager(Singleton):
    def __init__(self, config=_DEFAULT, window=_DEFAULT, game_state=_DEFAULT):
        self._config = config() or game.Config()
        self._config.load()
        self._window = window(self._config) or game.Window(self._config)
        self._game_state = game_state() or game.GameState()

    @classmethod
    def init_singleton(cls, *args, **kwargs):
        cls._singleton = cls(*args, **kwargs)
        return cls._singleton

    @property
    def config(self):
        return self._config

    @property
    def window(self):
        return self._window

    @property
    def game_state(self):
        return self._game_state
