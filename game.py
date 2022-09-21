# Placeholder class

from eventmanager import EventManager, EventListener
from models import Doctor, Dalek, Turn

class Game(EventListener):
    def __init__(self, eventmanager: EventManager):
        super().__init__(eventmanager)
        turns = [Doctor, Dalek]
        self.turn = Turn(turns)