# Debugging
import logging

# Events required
from eventmanager import EventManager, EventListener, Event, \
    BeginEvent, ExitEvent, TickEvent


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
        logging.info("Starting")
        while self.running:
            self.eventman.post(TickEvent())