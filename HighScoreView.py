from highscore import HighScore
from os import get_terminal_size# Get size of terminal
from os import system, name

class HighScoreView(object):

    def __init__(self, highscore : HighScore):
        self.highscore = highscore

    def afficher_header(self):
        posx = get_terminal_size().columns 
        print( "\n"+(("Date").center(int(posx*1/8)) + ("Nom").center(int(posx*1/8))+("Difficulte").center(int(posx*1/8) ) + ("Score").center(int(posx*1/8))).center(posx))

    def afficher_score(self,date,nom,dif,score):
        date = self.highscore.date 
        nom = self.highscore.nom 
        dif = self.highscore.difficulte 
        score = self.highscore.score
        posx = get_terminal_size().columns 
        print((date.center(int(posx*1/8)) + nom.center(int(posx*1/8))+dif.center(int(posx*1/8)) + score.center(int(posx*1/8))).center(posx))

    def afficher_tableau_score(self):
        system('cls')
        self.afficher_header()
        for i in range(len(self.highscore.liste_score)):
            score = str(self.highscore.get_score(self.highscore.liste_score[i]))
            nom =  self.highscore.get_nom(self.highscore.liste_score[i])
            dif =  self.highscore.get_diff(self.highscore.liste_score[i])
            date = self.highscore.get_date(self.highscore.liste_score[i])
            self.afficher_score(date, nom, dif, score)
        print('\n')
