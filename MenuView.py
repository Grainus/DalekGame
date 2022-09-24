from os import get_terminal_size
#peut etre faire de menuView et highScoreView des sous classes de GameView
 
class MenuView:

   def afficher_menu(self):

      print("\n"+("DALEK\n").center(get_terminal_size().columns)+"\n"+
      ("Choisissez vos options...").center(get_terminal_size().columns)+"\n"+
      " "*int(get_terminal_size().columns*1/6)+"Difficulte  1. Facile\n"+ 
      " "*int(get_terminal_size().columns*1/6+len("Difficulte  "))+"2: Moyen\n"+
      " "*int(get_terminal_size().columns*1/6+len("Difficulte  "))+"3. Difficile\n\n"+
      " "*int(get_terminal_size().columns*1/6)+"Mode de debug: (Fin ou 01) \n\n"+
      ("C = Case  D = Docteur X = Dalek   F = Ferraille").center(get_terminal_size().columns)+"\n\n"+
      ("APPUYEZ SUR ENTRE POUR CONTINUER...").center(get_terminal_size().columns)
      )

# catch EventManager debug O/N, difficultee: facile medium difficile
