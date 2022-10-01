"""Runs all components for debugging."""

from eventmanager import EventManager, DrawEvent
from controller import Keyboard
from game_engine import GameEngine
from game import Game
from models import Difficulty, PlayMode, State
from gameview import GameView
from MenuView import MenuView
from highscoreview import HighScoreView
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    evman = EventManager()
    evman.post(DrawEvent(State.MENU))
    
    while not (input := Keyboard.get_text()) in "123": pass
    diff = Difficulty(int(input) - 1)

    while not (input := Keyboard.get_text()) in "01": pass
    mode = PlayMode(int(input))

    game = Game(evman, difficulty=diff, play_mode=mode)

    kbd = Keyboard(evman, game)
    views = (
        GameView(evman, game),
        MenuView(evman),
        HighScoreView(evman)
    )
    engine = GameEngine(evman)
    engine.run()

if __name__ == '__main__':
    main()