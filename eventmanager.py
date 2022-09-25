# Type hinting and debugging
from __future__ import annotations 
from typing import List
import logging

# Thread management
from threading import Thread

# Enums used in events
from models import Direction, Ability, State


class Event(object):
    """Base class for events."""
    def __str__(self):
        return f"{self.__class__.__name__}{self.__dict__}"


class BeginEvent(Event):
    """Sent when a game starts."""


class ExitEvent(Event):
    """Sent when the game ends.
    
    Possible codes include:

        - 0 for a normal Game Over
        - 1 for an exit command during a game.
        - -1 for a critical error.
    """
    def __init__(self, exitcode: int = 0):
        self.code = exitcode


class TickEvent(Event):
    """Sent every game tick."""
    def __init__(self, state: State):
        self.state = state


class PlayerMoveEvent(Event):
    """Sent when a player needs to move."""
    def __init__(self, dir: Direction):
        self.dir = dir


class PlayerAbilityEvent(Event):
    """Sent when a player uses an ability or tool."""
    def __init__(self, ability: Ability):
        self.ability = ability


class DrawEvent(Event):
    """Sent when the display needs to be updated.

    This allows the game to not draw on every frame \
    if nothing is changing.
    """


class EventManager:
    """Communicates events between parts of the application.
    Also manages threads.
    """
    def __init__(self):
        self.listeners: List[EventListener] = []
    
    def register(self, component: EventListener) -> None:
        """Register a new listener that will receive events.
        The component needs to support a notify method.
        """
        if hasattr(component, 'notify') \
                and callable(component.notify):
            self.listeners.append(component)
        else:
            raise AttributeError
                
        
    def post(self, event: Event) -> None:
        """Broadcast an event to all listeners."""
        begin = isinstance(event, BeginEvent)
        for listener in self.listeners:
            if begin and listener.threaded:
                # Begin components in a new thread
                Thread(
                    target=listener.notify,
                    daemon=listener.daemon,
                    args=(event,)
                ).start()
            else:
                listener.notify(event)


class EventListener:
    """Base class for classes that listen to or broadcast events."""
    def __init__(self, eventmanager: EventManager):
        self.eventman = eventmanager # Allows posting
        eventmanager.register(self)  # Allows to be notified
        self.threaded = False        # By default, run in main thread
        self.daemon = False

    def notify(self, event: Event) -> None:
        """Callback when an event is posted."""
        if not isinstance(event, TickEvent):
            logging.debug(f"{event} received from {type(self)}")