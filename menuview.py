from os import get_terminal_size, system
#peut etre faire de menuView et highScoreView des sous classes de GameView

from eventmanager import EventListener, Event, DrawEvent
from models import State
from settings import CELL_REPR
 
class MenuView(EventListener):
    def notify(self, event: Event):
        if isinstance(event, DrawEvent):
            if event.state == State.MENU:
                MenuView.afficher_menu()
                
    @staticmethod
    def afficher_menu():
        # system('cls')
        termsize = get_terminal_size().columns
        termsix = termsize * 1/6
        diffoffset = " " * int(termsix + len("Difficulty  "))
        termsixoffset = " " * int(termsix)
        print(f"""
{"DALEK GAME".center(termsize)}
{"Choose your option...".center(termsize)}
{termsixoffset}Difficulty  1. Easy
{diffoffset}2. Medium
{diffoffset}3. Hard

{"Then choose your playmode...".center(termsize)}
{termsixoffset}Normal: 0
{termsixoffset}Debug:  1

{str(CELL_REPR)
    .replace("'", '')
    .replace("NoneType", "Empty")
    [1:-1].center(termsize)}

{"PRESS ENTER TO CONTINUE...".center(termsize)}
"""
        )