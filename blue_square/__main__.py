from blue_square import BlueSquareGameState, Config, Window
from game import main

main(
    _config=Config.get_instance(),
    _window=Window.get_instance(),
    _game_state=BlueSquareGameState.get_instance()
)
