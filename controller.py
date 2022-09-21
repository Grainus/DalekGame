# All required events
from eventmanager import EventManager, EventListener, \
    Event, TickEvent, PlayerMoveEvent, PlayerAbilityEvent

# Placeholder imports
from game import Game
from models import Doctor
from game_engine import Direction, Ability

# Input
from msvcrt import getch
from queue import SimpleQueue


class Keyboard(EventListener):
    """Controller that handles keyboard inputs and sends events"""
    def __init__(self, eventmanager: EventManager, game: Game):
        super().__init__(eventmanager)
        self.event_queue: SimpleQueue = SimpleQueue()
        self.game = game
        
    def notify(self, event: Event) -> None:
        if isinstance(event, TickEvent):
            # Check if it's currently the player's turn
            if self.game.turn.current() == Doctor:
                if not self.event_queue.empty():
                    self.eventman.post(self.event_queue.get())

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

        abilities = {
            'z': Ability.TELEPORT,
            'x': Ability.ZAP
        }

        while True:
            _input = getch()
            if ord(_input) == 0:
                _input = ord(getch())
                if _input in directions:
                    event = PlayerMoveEvent(directions[_input])
                    self.event_queue.put(event)
            else:
                _input = _input.decode().lower()
                if _input in abilities.keys():
                    event = PlayerAbilityEvent(abilities[_input])
                    self.event_queue.put(event)