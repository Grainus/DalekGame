from eventmanager import *
from controller import *
from game_engine import *
from game import *
from models import *
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    evman = EventManager()
    game = Game(evman)
    kbd = Keyboard(evman, game)
    engine = GameEngine(evman)
    engine.run()

if __name__ == '__main__':
    main()