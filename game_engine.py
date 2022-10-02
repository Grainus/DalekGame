# Debugging
import logging

# Events required
from eventmanager import EventManager, EventListener, Event, \
    BeginEvent, ExitEvent, TickEvent

from models import State

class GameEngine(EventListener):
    """Makes the game run from behind the scenes."""
    def __init__(self, eventmanager: EventManager):
        super().__init__(eventmanager)
        self.running = False
        self.state: State
    
    def notify(self, event: Event) -> None:
        super().notify(event)
        if isinstance(event, ExitEvent):
            if event.code == 0:
                self.state = State.GAMEOVER
                self.running = False
            elif event.code == 1:
                self.state = State.MENU
            else:
                self.running = False
    
    def run(self) -> None:
        """Starts the main game loop."""
        self.running = True
        self.state = State.PLAY
        self.eventman.post(BeginEvent())
        logging.info("Starting")
        while self.running:
            self.eventman.post(
                TickEvent(self.state)
            )