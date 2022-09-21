from eventmanager import EventManager, EventListener, Event, TickEvent, PlayerMoveEvent, PlayerAbilityEvent
#from game import Game
from game_engine import Direction, Ability

# Input
from msvcrt import getch
from queue import SimpleQueue

class Keyboard(EventListener):
    """Controller that handles keyboard inputs and sends events"""
    def __init__(self, eventmanager: EventManager, game):
        super().__init__(eventmanager)
        self.input_queue: SimpleQueue = SimpleQueue()
        self.game = game
        
    def notify(self, event: Event) -> None:
        if isinstance(event, TickEvent):
            if self.game.turn[self.game.turnindex]:
                if not self.input_queue.empty():
                    input = self.input_queue.get()
                    if isinstance(input, Direction):
                        self.eventman.post(PlayerMoveEvent(input))
                    elif isinstance(input, Ability):
                        self.eventman.post(PlayerAbilityEvent(input))
                        
    def run(self):
        directions = {
            72: Direction.UP,
            73: Direction.UPRIGHT,
            77: Direction.RIGHT,
            81: Direction.DOWNRIGHT,
            80: Direction.DOWN,
            79: Direction.DOWNLEFT,
            75: Direction.LEFT,
            71: Direction.UPLEFT
        }
        while True:
            _input = getch()
            if ord(_input) == 0:
                _input = ord(getch())
                if _input in directions:
                    print(directions[_input])