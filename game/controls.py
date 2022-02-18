from enum import auto


class Controls:
    QUIT = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    SPRINT = auto()


for key, value in Controls.__dict__.items():
    if isinstance(value, auto):
        setattr(Controls, key, key)
