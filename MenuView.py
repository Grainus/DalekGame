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
        termsix = termsize * 1/6
        diffoffset = " " * int(termsix + len("Difficulty  "))
        print(f"""
{"DALEK GAME".center(termsize)}
{"Choose your option...".center(termsize)}
{" " * int(termsix)}Difficulty  1. Easy
{diffoffset}2. Medium
{diffoffset}3. Hard

{" " * int(termsix)}Debug mode: (Fin ou 01)


{"C = Case  D = Doctor  X = Dalek  J = Junk".center(termsize)}


{"PRESS ENTER TO CONTINUE...".center(termsize)}
"""
        )
        
MenuView.afficher_menu()