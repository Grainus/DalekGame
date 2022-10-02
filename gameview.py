from os import get_terminal_size, system

# Enable virtual terminal processing
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

import re
from game import Game
from eventmanager import EventManager, EventListener, Event, DrawEvent
from models import State, Difficulty
from settings import CELL_CHAR, CELL_COLOR

def color(code: int, string: str) -> str:
    return f"\033[{code}m{string}\033[0m"

class GameView(EventListener):
    def __init__(self, eventmanager: EventManager, game : Game):
        super().__init__(eventmanager)
        self.game = game
        
    
    def notify(self, event: Event) -> None:
        if isinstance(event, DrawEvent):
            if event.state == State.PLAY:
                self.show_game_view()
    
    def _get_vars(self) -> tuple:
        termsize = get_terminal_size()
        between_x = int(termsize.columns * 1/50)
        between_y = int(termsize.lines / 50)
        width  = int(termsize.columns / self.game.grid.width / 3)
        height  = int(termsize.lines / self.game.grid.height / 1.5)
        return between_x, between_y, width, height

    def afficher_header(self, niveau, score):
        diff = self.game.difficulty.name.title()
        posx = get_terminal_size().columns 
        print()
        print( (f"Difficulty: {diff}").center(int(posx*1/3)) +(f"Niveau: {niveau}").center(int((posx * 1/3))) + (f"Score: {score}").center(int(posx*1/3)))
        print()

    

    def afficher_les_cases(self, grid):
        between_x, between_y, width, height = self._get_vars()
        #Boucle pour string des cases, une fois qu'on a la string il faut simplement la print(string) n fois pour faire la heuteur de la case
        sep = " " * between_x
        for row in grid.cells: 
            output = "" 
            for cell in row:
                output += CELL_CHAR[type(cell).__name__] * width + sep

            output = output.rstrip()
            output = output.center(get_terminal_size().columns)
            for celltype, char in CELL_CHAR.items():
                output = re.sub(
                    rf'({char}+)',
                    lambda x: color(CELL_COLOR[celltype], x.group()),
                    output
                )
            for _ in range(height):
                print(output)
            print('\n' * between_y, end='')  

    @staticmethod
    def afficher_footer(difficulte, nb_de_zap): 
        if (difficulte == Difficulty.EASY):
            sorte_de_teleporteur = "Safe"
        if (difficulte == Difficulty.MEDIUM):
            sorte_de_teleporteur = "Normal"
        if (difficulte == Difficulty.HARD):   
            sorte_de_teleporteur = "Dangerous"
            
        posx = get_terminal_size().columns 
        print( ("TELEPORTEUR (z) : " + sorte_de_teleporteur).center(int(posx*1/3)) + (" ").center(int(posx*1/3))+ 
        (f"ZAP (x): [{nb_de_zap}]").center(int(posx*1/3))+"\n")

    def show_game_view(self):
        grid = self.game.grid
        row = self.game.grid.width
        col = self.game.grid.height
        #les param de Game a renommer
        difficulte = self.game.difficulty
        niveau = self.game.level
        score = self.game.score
        nb_de_zap = self.game.doctor.zap_count
        system('cls')
        self.afficher_header(niveau, score)
        self.afficher_les_cases(grid)
        GameView.afficher_footer(difficulte, nb_de_zap)
