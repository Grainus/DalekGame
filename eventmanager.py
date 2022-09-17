from game_engine import Direction, Ability

class Event(object):
    """Base class for events"""
    pass


class ExitEvent(Event):
    """Sent when the game ends
    
    Possible codes include:

         0 for a normal Game Over.
         1 for an exit command during a game.
        -1 for a critical error.
    """
    def __init__(self, exitcode: int = 0):
        self.code = exitcode


class BeginEvent(Event):
    """Sent when a game starts"""
    pass


class PlayerMoveEvent(Event):
    """Sent when a player needs to move"""
    def __init__(self, dir: Direction):
        self.dir = dir


class PlayerAbilityEvent(Event):
    """Sent when a player uses an ability or tool"""
    def __init__(self, ability: Ability):
        self.type = ability


class UpdateEvent(Event):
    """Sent when the display needs to be updated"""
    pass


class EventManager:
    """Communicates events between parts of the application."""
    def __init__(self):
        self.listeners = []
    
    def register(self, component) -> None:
        """Register a new listener that will receive events.
        The component needs to support a notify method."""
        if hasattr(component, 'notify') \
                and callable(component.notify):
            self.listeners.append(component)
        else:
            raise AttributeError
                
        
    def post(self, event: Event) -> None:
        """Broadcast an event to all listeners."""
        for listener in self.listeners:
            listener.notify(event)