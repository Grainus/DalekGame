
from operator import is_
from eventmanager import BeginEvent, Event,ExitEvent,EventManager,EventListener, PlayerAbilityEvent
from models import Doctor, Dalek, Ability, Junk
from grid import GameGrid
from enum import Enum

class Turn(Enum):
    DOCTOR = 0
    DALEK = 1

class Difficulty(Enum):
    FACILE =0
    MOYEN =1
    DIFFICILE =2 

class PlayMode(Enum):
    NORMAL = 0
    DEBUG = 1

class Game:
    
    def __init__(self, event_manager: EventManager,grid :GameGrid, difficulty : Difficulty, play_mode : PlayMode):

        self.difficulty=difficulty
        self.play_mode=play_mode

        self.score=0
        self.wave_number = 1

        self.turn= Turn.DOCTOR

        self.doctor = Doctor()
        self.grid = grid
    
    def start_game(self):
        self.grid.summon_daleks(5*self.wave_number)
        self.grid.summon_doctor()
        self.start_wave()
    
    def end_game(self):
        pass

    def start_wave(self):
        self

    def end_wave(self):
        self.wave_number+=1

    def start_round(self):
        self.turn=Turn.DOCTOR

    def end_round(self):
        self.update_score()

    def update_score(self)->int:
        return (5*self.wave_number) - (self.grid.get_all_daleks().length)

    def check_teleport(self):
        if(self.difficulty == Difficulty.FACILE):
            is_pos_found = False
            pos = []
            while not(is_pos_found):
                pos = self.grid.new_pos([],'TELEPORT')
                is_pos_found = True
                for i in range(-2,3):
                    for j in range(-2,3):
                        if isinstance(self.grid.grid[pos[0]+i][pos[1]+j],Dalek):
                            is_pos_found = False
                if (is_pos_found):
                    if isinstance(self.grid.grid[pos[0]][pos[1]],Junk):
                        is_pos_found = False
            self.grid.make_move(self.grid.find_doctor(),pos)
        
        if(self.difficulty == Difficulty.MOYEN):
            is_pos_found = False
            pos = []
            while not (is_pos_found):
                pos = self.grid.new_pos([],'TELEPORT')
                if not isinstance(self.grid.grid[pos[0]][pos[1]],Junk):
                    if not isinstance(self.grid.grid[pos[0]][pos[1]],Dalek):
                        is_pos_found = True
            self.grid.make_move(self.grid.find_doctor(),pos)

        if(self.difficulty == Difficulty.DIFFICILE):
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
        if isinstance(event, PlayerAbilityEvent):
            self.use_tool(event.ability)
        if isinstance(event,BeginEvent):
            self.start_game()
        if isinstance(event,ExitEvent):
            self.end_game()

        
    