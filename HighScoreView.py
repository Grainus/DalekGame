from os import get_terminal_size, system

from highscore import HighScore
from eventmanager import EventManager, EventListener, Event, DrawEvent
from models import State

class HighScoreView(EventListener):
    
    def notify(self, event: Event):
        if isinstance(event, DrawEvent):
            if event.state == State.HIGHSCORE:
                HighScoreView.afficher_tableau_score()
    
    @staticmethod
    def afficher_header() -> None:
        posx = get_terminal_size().columns 
        print( "\n"+(("Date").center(int(posx*1/8)) + ("Nom").center(int(posx*1/8))+("Difficulte").center(int(posx*1/8) ) + ("Score").center(int(posx*1/8))).center(posx))

    @staticmethod
    def afficher_score(scoretuple) -> None:
        dif, name, score, date = scoretuple
        posx = get_terminal_size().columns 
        print(
            (
                date.center(int(posx*1/8))
                + name.center(int(posx*1/8))
                + dif.center(int(posx*1/8))
                + score.center(int(posx*1/8))
            ).center(posx)
        )

    @staticmethod
    def afficher_tableau_score() -> None:
        system('cls')
        HighScoreView.afficher_header()
        scores = HighScore.get_scores()
        if scores is not None:
            for score in scores:
                HighScoreView.afficher_score(score)
        print('\n')