import datetime 
from game import Game
#import Game

class HighScore():
   def __init__(self, game: Game):
      self.game = game
      self.liste_score = []
   
   def get_score(liste):
      return liste['score']
   def get_nom(liste):
      return liste['nom']
   def get_diff(liste):
      return liste['difficulte']
   def get_date(liste):
      return liste['date']
   
   def demander_nom():
      print()
      nom = input("Nom: ")
      return nom   

   #pour que la liste aille toujours le high score en premier
   def push_score(self):
      if ( self.game.difficulty == 0):
         difficulte = "Facile"
      if ( self.game.difficulty == 1):
         difficulte = "Moyen"
      if ( self.game.difficulty == 2):
         difficulte = "Difficile"
      nom = self.demander_nom()
      score = self.game.score
      date = str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)
      new_score = {'date': date, 'nom':nom, 'difficulte':difficulte,'score': score}
      self.liste_score.append(new_score)
      self.liste_score.sort(reverse = True, key = self.get_score)
