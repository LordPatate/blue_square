from singleton import Singleton


class ContextManager(Singleton):
    def __init__(self, config, controls, window, game_state):
        self._config = config
        self._controls = controls
        self._window = window
        self._game_state = game_state

    @classmethod
    def init_singleton(cls, *args, **kwargs):
        cls._singleton = cls(*args, **kwargs)

    @property
    def config(self):
        return self._config

    @property
    def controls(self):
        return self._controls

    @property
    def window(self):
        return self._window

    @property
    def game_state(self):
        return self._game_state
