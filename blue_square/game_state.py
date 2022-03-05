from math import sqrt

from blue_square import Const, Controls
from game import ContextManager, GameState

HORIZONTAL = Controls.LEFT, Controls.RIGHT
VERTICAL = Controls.UP, Controls.DOWN
ORTH = {
    key: (VERTICAL if key in HORIZONTAL else HORIZONTAL)
    for key in (HORIZONTAL + VERTICAL)
}


class BlueSquareGameState(GameState):
    def __init__(self):
        self.blue_square_pos = [0, 0]
        self.walls = {
            "top": (0, -400),
            "bot": (0, 400),
            "left": (-400, 0),
            "right": (400, 0),
        }

    def update(self):
        super().update()
        context = ContextManager.get_instance()
        controls = context.controls

        def _step_toward(direction):
            if not controls.is_pressed(direction):
                return 0
            step = (
                Const.PLAYER_SPRINT
                if controls.is_pressed(Controls.SPRINT)
                else Const.PLAYER_STEP
            )
            diagonal_factor = (
                sqrt(2) / 2
                if any(controls.is_pressed(orth) for orth in ORTH[direction])
                else 1
            )
            return round(step * diagonal_factor)
        self.blue_square_pos[0] += (_step_toward(Controls.RIGHT)
                                    - _step_toward(Controls.LEFT))
        self.blue_square_pos[1] += (_step_toward(Controls.DOWN)
                                    - _step_toward(Controls.UP))

    def on_exit(self):
        pass
