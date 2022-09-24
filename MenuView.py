from re import X
from os import get_terminal_size
#peut etre faire de menuView et highScoreView des sous classes de GameView
 
class MenuView:

   def afficher_menu(self, difficulte):
      difficulte_choisi = ""
      if(difficulte == '1'):
         difficulte_choisi = "Facile"
      elif(difficulte == '2'):
         difficulte_choisi = "Moyen"
      elif(difficulte == '3'):
         difficulte_choisi = "Difficile"

      print("\n"+("DALEK\n").center(get_terminal_size().columns)+"\n"+
      ("Choisissez vos options...").center(get_terminal_size().columns)+"\n"+
      " "*int(get_terminal_size().columns*1/6)+"Difficulte  1. Facile\n"+ 
      " "*int(get_terminal_size().columns*1/6+len("Difficulte  "))+"2: Moyen\n"+
      " "*int(get_terminal_size().columns*1/6+len("Difficulte  "))+"3. Difficile\n\n"+
      " "*int(get_terminal_size().columns*1/6)+"Difficulte choisi: "+difficulte_choisi+"\n\n"+
      " "*int(get_terminal_size().columns*1/6)+"Mode de debug: (Fin ou 01) \n\n"+
      ("C = Case  D = Docteur X = Dalek   F = Ferraille").center(get_terminal_size().columns)+"\n\n"+
      ("APPUYEZ SUR ENTRE POUR CONTINUER...").center(get_terminal_size().columns)
      )

MenuView().afficher_menu('1')
# catch EventManager debug O/N, difficultee: facile medium difficile