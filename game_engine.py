from eventmanager import EventManager, EventListener, Event, \
    ExitEvent, BeginEvent, TickEvent

class GameEngine(EventListener):
    def __init__(self, eventmanager: EventManager):
        super().__init__(eventmanager)
        self.running = False
    
    def notify(self, event: Event) -> None:
        super().notify(event)
        if isinstance(event, ExitEvent):
            self.running = False
    
    def run(self) -> None:
        self.running = True
        self.eventman.post(BeginEvent())
        print("Starting")
        while self.running:
            self.eventman.post(TickEvent())