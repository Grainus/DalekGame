"""Runs all components for debugging."""

from eventmanager import EventManager
from controller import Keyboard
from game_engine import GameEngine
from game import Game
from models import Difficulty, PlayMode
from gameview import GameView
from MenuView import MenuView
from highscoreview import HighScoreView
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    evman = EventManager()
    game = Game(evman, Difficulty.HARD, PlayMode.NORMAL)
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