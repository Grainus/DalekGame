"""Runs all components for debugging."""

from pickle import NONE
from eventmanager import DrawEvent, EventManager, State
from controller import Keyboard
from game_engine import GameEngine
from game import Game
from gameview import GameView
from models import Difficulty
from grid import GameGrid
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    evman = EventManager()
    grid = GameGrid(10,10)
    
    evman.post(DrawEvent(State.MENU))
    inputValid = False
    input = None
    while not inputValid:
        input = Keyboard.get_text()
        if input == '1':
            inputValid = True
            input = Difficulty.EASY
        elif input == '2':
            inputValid = True
            input = Difficulty.MEDIUM
        elif input == '3':
            inputValid = True
            input = Difficulty.HARD
    game = Game(evman,grid,input)
    kbd = Keyboard(evman, game)
    engine = GameEngine(evman)
    game_view = GameView(evman, game)

    engine.run()

if __name__ == '__main__':
    main()