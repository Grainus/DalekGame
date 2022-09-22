# Typing
from typing import NoReturn

# Input
from msvcrt import getch
from queue import SimpleQueue

# Required events
from eventmanager import EventManager, EventListener, Event, \
    BeginEvent, TickEvent, PlayerMoveEvent, PlayerAbilityEvent

# Placeholder imports
from game import Game
from models import Doctor, Direction, Ability


class Keyboard(EventListener):
    """Controller that handles keyboard inputs and sends events."""
    def __init__(self, eventmanager: EventManager, game: Game):
        super().__init__(eventmanager)
        self.event_queue: SimpleQueue = SimpleQueue()
        self.game = game
        self.threaded = True
        self.daemon = True
        
    def notify(self, event: Event) -> None:
        super().notify(event)
        if isinstance(event, BeginEvent):
            self.run()
        elif isinstance(event, TickEvent):
            # Check if it's currently the player's turn
            if self.game.turn.current() == Doctor:
                if not self.event_queue.empty():
                    self.eventman.post(self.event_queue.get())

    def run(self) -> NoReturn:
        """Run the input loop forever.
        Inputs are recorded constantly but sent at most once per tick.
        """
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
                _inputval = ord(getch())
                if _inputval in directions:
                    self.event_queue.put(
                        PlayerMoveEvent(directions[_inputval])
                    )
            else:
                _inputstr = _input.decode().lower()
                if _inputstr in abilities:
                    self.event_queue.put(
                        PlayerAbilityEvent(abilities[_inputstr])
                    )