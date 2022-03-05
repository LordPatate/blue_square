from game import ContextManager, Controls, Quit


class GameState:
    def update(self):
        context = ContextManager.get_instance()
        controls = context.controls

        if controls.is_pressed(Controls.QUIT):
            raise Quit

    def on_exit(self):
        pass
