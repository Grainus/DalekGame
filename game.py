"""Main game logic, handles turns and waves."""

from eventmanager import Event, EventManager, EventListener, \
    BeginEvent, ExitEvent, PlayerMoveEvent, PlayerAbilityEvent, \
    DrawEvent
from models import Doctor, Ability, Junk, Dalek, \
    Difficulty, PlayMode, State
from grid import GameGrid
from enum import Enum


class Game(EventListener):
    def __init__(self, eventmanager: EventManager,
            difficulty: Difficulty, play_mode: PlayMode):
        super().__init__(eventmanager)

        self.difficulty = difficulty
        self.play_mode = play_mode

        self.score = 0
        self.level = 1

        self.doctor = Doctor()
    
    def start_game(self):
        self.grid = GameGrid()
        self.grid.summon_doctor()
        self.start_wave()

    def start_wave(self):
        self.doctor.zap_count += 1
        self.grid.summon_daleks(5*self.level)
        self.eventman.post(DrawEvent(State.PLAY))
        
    def end_wave(self):
        self.level+=1
        #self.start_wave() to be added depending on the working of game engine

    def start_round(self,dir = None):
        if dir is not None:
            self.grid.request_move(dir)
        self.grid.move_all_daleks()
        self.score = self.update_score()
        if self.grid.find_doctor() is False:
            self.eventman.post(ExitEvent)#verify is doctor is dead
        if self.grid.get_all_daleks() is None:
            self.end_wave()
            self.start_wave()
        
        self.eventman.post(DrawEvent(State.PLAY))

    def end_round(self):
        self.score = self.update_score()

    def update_score(self)->int:
        return ((5*self.level) - (len(self.grid.get_all_daleks()))) * 5 #(nombre de daleks initial - nombre de dalek vivant) * 5 points par dalek mort

    def check_teleport(self):
        if(self.difficulty == Difficulty.EASY):
            is_pos_found = False
            pos = []
            n=0
            while not(is_pos_found) or (n < 100):
                pos = self.grid.new_pos([],'TELEPORT')
                is_pos_found = True
                n+=1#pour pas rester stuck dans la while loop
                for i in range(-2,3):
                    for j in range(-2,3):
                        if isinstance(self.grid.grid[pos[0]+i][pos[1]+j],Dalek):
                            is_pos_found = False
                if (is_pos_found):
                    if isinstance(self.grid.grid[pos[0]][pos[1]],Junk):
                        is_pos_found = False
            self.grid.make_move(self.grid.find_doctor(),pos)
            
        if(self.difficulty == Difficulty.MEDIUM):
            is_pos_found = False
            pos = []
            while not (is_pos_found):
                pos = self.grid.new_pos([],'TELEPORT')
                if not isinstance(self.grid.cells[pos[0]][pos[1]],Junk):
                    if not isinstance(self.grid.grid[pos[0]][pos[1]],Dalek):
                        is_pos_found = True
            self.grid.make_move(self.grid.find_doctor(),pos)

        if(self.difficulty == Difficulty.HARD):
            is_pos_found = False
            pos = []
            while not (is_pos_found):
                pos = self.grid.new_pos([],'TELEPORT')
                if not isinstance(self.grid.grid[pos[0]][pos[1]],Junk):
                    is_pos_found = True
            self.grid.make_move(self.grid.find_doctor(),pos)
                

    
    def zap(self,pos):
        if (self.doctor.can_zap()):
            for i in range(-1,2):
                for j in range(-1,2):
                    if not((i == pos[0])and(j==pos[1])):
                        self.grid.kill_at([pos[0]+i,pos[1]+j])

    def use_tool(self,ability: Ability):
        if(ability == ability.ZAP):
            self.zap(self.grid.find_doctor())
        if(ability == ability.TELEPORT):
            self.check_teleport()

    def notify(self,event: Event):
        super().notify(event)
        if isinstance(event,BeginEvent):
            self.start_game()
        elif isinstance(event, PlayerMoveEvent):
            self.start_round(event.dir)
        if isinstance(event, PlayerAbilityEvent):
            self.use_tool(event.ability)
        
