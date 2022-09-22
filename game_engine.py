# Debugging
import logging

# Events required
from eventmanager import EventManager, EventListener, Event, \
    ExitEvent, BeginEvent, TickEvent


class GameEngine(EventListener):
    """Makes the game run from behind the scenes."""
    def __init__(self, eventmanager: EventManager):
        super().__init__(eventmanager)
        self.running = False
    
    def notify(self, event: Event) -> None:
        super().notify(event)
        if isinstance(event, ExitEvent):
            self.running = False
    
    def run(self) -> None:
        """Starts the main game loop."""
        self.running = True
        self.eventman.post(BeginEvent())
        logging.debug("Starting")
        while self.running:
            self.eventman.post(TickEvent())