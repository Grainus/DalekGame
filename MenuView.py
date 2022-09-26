from os import get_terminal_size, system
#peut etre faire de menuView et highScoreView des sous classes de GameView

from eventmanager import EventListener, Event, DrawEvent
from models import State
 
class MenuView(EventListener):
    def notify(self, event: Event):
        if isinstance(event, DrawEvent):
            if event.state == State.MENU:
                MenuView.afficher_menu()
                
    @staticmethod
    def afficher_menu():
        system('cls')
        termsize = get_terminal_size().columns
        print("\n"+("DALEK GAME\n").center(termsize)+"\n"+
        ("Choose your option...").center(termsize)+"\n"+
        " "*int(termsize*1/6)+"Difficulty  1. Easy\n"+ 
        " "*int(termsize*1/6+len("Difficulty  "))+"2: Medium\n"+
        " "*int(termsize*1/6+len("Difficulty  "))+"3. Hard\n\n"+
        " "*int(termsize*1/6)+"Debug mode: (Fin ou 01) \n\n"+
        ("C = Case  D = Doctor  X = Dalek  J = Junk").center(termsize)+"\n\n"+
        ("PRESS ENTER TO CONTINUE...").center(termsize)+"\n")
