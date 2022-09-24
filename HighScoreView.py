import HighScore

# Get size of terminal
from os import get_terminal_size
from os import system, name
import datetime 

# required 
#from game import Game #juste nom du joueur a la fin de la partie, score et niveau de difficultee

class HighScoreView(object):
    # vu que c'est un objet peut etre mettre les parametres qui changent en __init__?

    def afficher_header(self):
        posx = get_terminal_size().columns 
        print( (("Date").center(int(posx*1/8)) + ("Nom").center(int(posx*1/8))+("Difficulte").center(int(posx*1/8) ) + ("Score").center(int(posx*1/8))).center(posx))

    def afficher_score(self, nom, difficulte, score):
        posx = get_terminal_size().columns 
        date = str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)
        print((date.center(int(posx*1/8)) + nom.center(int(posx*1/8))+difficulte.center(int(posx*1/8)) + score.center(int(posx*1/8))).center(posx))

HighScoreView().afficher_header()
HighScoreView().afficher_score("kevin", "moyen", "4" ) 
HighScoreView().afficher_score("kevin", "difficile", "4" )  




