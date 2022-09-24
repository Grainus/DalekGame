import HighScore
from os import get_terminal_size# Get size of terminal
from os import system, name

class HighScoreView(object):

    def afficher_header(self):
        posx = get_terminal_size().columns 
        print( (("Date").center(int(posx*1/8)) + ("Nom").center(int(posx*1/8))+("Difficulte").center(int(posx*1/8) ) + ("Score").center(int(posx*1/8))).center(posx))

    def afficher_score(self, date, nom, difficulte, score):
        posx = get_terminal_size().columns 
        print((date.center(int(posx*1/8)) + nom.center(int(posx*1/8))+difficulte.center(int(posx*1/8)) + score.center(int(posx*1/8))).center(posx))

def afficher_tableau_score():
    HighScoreView().afficher_header()
    for i in range(len(HighScore.HighScore().liste_score)):
        score = str(HighScore.HighScore.get_score(HighScore.HighScore().liste_score[i]))
        nom =  HighScore.HighScore.get_nom(HighScore.HighScore().liste_score[i])
        dif =  HighScore.HighScore.get_diff(HighScore.HighScore().liste_score[i])
        date = HighScore.HighScore.get_date(HighScore.HighScore().liste_score[i])
        HighScoreView().afficher_score(date, nom, dif, score)
