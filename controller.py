"""Handles input for the program.

These classes should be run in a separate thread if they are blocking.

Todo:
    * Get input from joysticks
"""

# Typing
from typing import Dict, NoReturn

# Input
from msvcrt import getch
from queue import SimpleQueue

# Required events
from eventmanager import EventManager, EventListener, Event, \
    BeginEvent, TickEvent, PlayerMoveEvent, PlayerAbilityEvent

# Placeholder imports
from game import Game
from models import Doctor, Direction, Ability, State


class Keyboard(EventListener):
    """Controller that handles keyboard inputs and sends events."""
    def __init__(self, eventmanager: EventManager, game: Game):
        super().__init__(eventmanager)
        self.event_queue: SimpleQueue = SimpleQueue()
        self.game = game
        self.state: State
        self.threaded = True
        self.daemon = True
        
    def notify(self, event: Event) -> None:
        super().notify(event)
        if isinstance(event, BeginEvent):
            self.run()
        elif isinstance(event, TickEvent):
            self.state = event.state
            if event.state == State.PLAY:
                # Check if it's currently the player's turn
                # if self.game.turn.current() == Doctor:
                if not self.event_queue.empty():
                    self.eventman.post(self.event_queue.get())
            elif event.state == State.GAMEOVER:
                self.event_queue = SimpleQueue() # Clear queue
            

    def run(self) -> NoReturn:
        """Run the input loop forever.
        Inputs are recorded constantly but sent at most once per tick.
        """
        directions: Dict[int | str, Direction] = {
            **dict.fromkeys([72, '8'], Direction.UP),
            **dict.fromkeys([73, '9'], Direction.UPRIGHT),
            **dict.fromkeys([77, '6'], Direction.RIGHT),
            **dict.fromkeys([81, '3'], Direction.DOWNRIGHT),
            **dict.fromkeys([80, '2'], Direction.DOWN),
            **dict.fromkeys([79, '1'], Direction.DOWNLEFT),
            **dict.fromkeys([75, '4'], Direction.LEFT),
            **dict.fromkeys([71, '7'], Direction.UPLEFT),
            **dict.fromkeys(['\r', '5'], Direction.NONE)
        }

        abilities = {
            'z': Ability.TELEPORT,
            'x': Ability.ZAP
        }

        while True:
            if self.state == State.PLAY:
                _inputbyte = getch()
                _input: int | str
                if ord(_inputbyte) == 0: # Arrow keys
                    _input = ord(getch())
                else:
                    _input = _inputbyte.decode().lower()

                if _input in directions:
                    self.event_queue.put(
                        PlayerMoveEvent(directions[_input])
                    )
                elif _input in abilities:
                    self.event_queue.put(
                        PlayerAbilityEvent(abilities[_input]) # type: ignore
                    )

    @staticmethod
    def get_text() -> str:
        return input()