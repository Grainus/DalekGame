from os import get_terminal_size, system

from game import Game
from eventmanager import EventManager, EventListener, Event, DrawEvent
from models import State, Difficulty, Doctor, Dalek, Junk

class GameView(EventListener):
    def __init__(self, eventmanager: EventManager, game : Game):
        super().__init__(eventmanager)
        self.game = game
        
    
    def notify(self, event: Event) -> None:
        if isinstance(event, DrawEvent):
            if event.state == State.PLAY:
                self.show_game_view()
    
    @staticmethod
    def _get_vars() -> tuple:
        termsize = get_terminal_size()
        between_x = int(termsize.columns * 1/50)
        between_y = int(termsize.lines * 1/20)
        width  = int(termsize.columns * 1/30)
        height  = int(termsize.columns * 1/55)
        return between_x, between_y, width, height

    def afficher_header(self, niveau, score):
        diff = self.game.difficulty.name.title()
        posx = get_terminal_size().columns 
        print()
        print( (f"Difficulty: {diff}").center(int(posx*1/3)) +(f"Niveau: {niveau}").center(int((posx * 1/3))) + (f"Score: {score}").center(int(posx*1/3)))
        print()

    @staticmethod
    def afficher_les_cases(grid):
        between_x, between_y, width, height = GameView._get_vars()
        #Boucle pour string des cases, une fois qu'on a la string il faut simplement la print(string) n fois pour faire la heuteur de la case
        sep = " " * between_x
        for row in grid.cells: 
            output = "" 
            for cell in row:
                if isinstance(cell, Doctor):
                    output += "X" * width + sep
                elif isinstance(cell, Junk):
                    output += "J" * width + sep
                elif isinstance(cell, Dalek):
                    output += "D" * width + sep
                else:
                    output += "C" * width + sep
                    
            for i in range(height):
                #Ne pas oublier d'enlever le "  " a la fin des strings quand on affiche le jeu bien centrer ex: "CCCCC  CCCCC  " -> "CCCCC  CCCCC"
                # you mean rstrip() ??
                print(output.center(get_terminal_size().columns - between_x))
            print('\n' * between_y)  

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
        GameView.afficher_les_cases(grid)
        GameView.afficher_footer(difficulte, nb_de_zap)
