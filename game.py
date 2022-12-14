"""Main game logic, handles turns and waves."""

from time import sleep
from eventmanager import Event, EventManager, EventListener, \
    BeginEvent, ExitEvent, PlayerMoveEvent, PlayerAbilityEvent, \
    DrawEvent, TickEvent
from models import Doctor, Ability, Dalek, Difficulty, PlayMode, State
from grid import GameGrid


class Game(EventListener):
    def __init__(self, eventmanager: EventManager,
            difficulty: Difficulty, play_mode: PlayMode):
        super().__init__(eventmanager)

        self.difficulty = difficulty
        self.play_mode = play_mode

        self.score = 0
        self.level = 0

        self.doctor = Doctor()
    
    def start_game(self):
        self.grid = GameGrid()
        self.grid.summon_doctor()
        self.start_wave()

    def start_wave(self):
        self.doctor.zap_count += 1
        self.level += 1
        self.grid.summon_daleks(5*self.level)
        self.eventman.post(DrawEvent(State.PLAY))

    def start_round(self,dir = None):
        if dir is not None:
            self.grid.request_move(dir)
        if not (self.play_mode is PlayMode.DEBUG_WAIT 
                and self.grid.can_die_next()):
            self.grid.move_all_daleks()
            self.score = self.update_score()
            if not self.grid.find_doctor():
                self.eventman.post(ExitEvent()) # Check if doctor is dead
            if not self.grid.find_pos(Dalek):
                self.start_wave()
        self.end_round()

    def end_round(self):
        self.eventman.post(DrawEvent(State.PLAY))
        if (not self.grid.find_doctor() 
                or (self.play_mode is PlayMode.DEBUG_WAIT 
                    and self.grid.can_die_next())):
            self.eventman.post(ExitEvent())
        else:
            self.score = self.update_score()

    def update_score(self) -> int:
        beaten = self.level - 1
        cumm_points = 5 * ((beaten + 1) * beaten // 2)
        killed_now = 5 * self.level - len(self.grid.get_all_daleks())
        return cumm_points + killed_now
    
    def zap(self, pos):
        if (self.doctor.can_zap()):
            self.doctor.zap_count -= 1
            for i in range(-1, 2):
                for j in range(-1, 2):
                    killpos = (pos[0]+i, pos[1]+j)
                    if self.grid.is_inside(killpos) and killpos != pos:
                        self.grid.kill_at(killpos)

    def use_tool(self,ability: Ability):
        if(ability == ability.ZAP):
            self.zap(self.grid.find_doctor())
        if(ability == ability.TELEPORT):
            self.grid.teleport_doctor(self.difficulty)
        self.start_round()

    def notify(self,event: Event):
        super().notify(event)
        if isinstance(event,BeginEvent):
            self.start_game()
        if self.play_mode is PlayMode.NORMAL:
            if isinstance(event, PlayerMoveEvent):
                self.start_round(event.dir)
            elif isinstance(event, PlayerAbilityEvent):
                self.use_tool(event.ability)
        else:
            if isinstance(event, TickEvent):
                sleep(2) # Blocking call :/
                self.start_round()
