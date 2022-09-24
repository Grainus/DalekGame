import datetime 
import Game

class HighScore():
   liste_score = []
   def get_score(liste):
      return liste['score']
   def get_nom(liste):
      return liste['nom']
   def get_diff(liste):
      return liste['difficulte']
   def get_date(liste):
      return liste['date']
   #pour que la liste aille toujours le high score en premier
   
def push_score():
   difficulte = Game.Game().difficulte
   nom = Game.Game().nom
   score = Game.Game().score
   date = str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)
   new_score = {'date': date, 'nom':nom, 'difficulte':difficulte,'score': score}
   HighScore().liste_score.append(new_score)
   HighScore().liste_score.sort(reverse = True, key = HighScore.get_score)
