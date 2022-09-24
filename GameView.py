from os import get_terminal_size
import GameGrid
import Game

class GameView():
   def __init__(self, espace_entre_cases = 2, largeur_case = 5):
        self.espace_entre_cases =  espace_entre_cases
        self.largeur_case  = largeur_case        

    def afficher_header(self, difficulte, niveau, score):
        posx = get_terminal_size().columns 
        print()
        print( ("Difficulte: "+difficulte).center(int(posx*1/3)) +("Niveau: " + niveau).center(int((posx * 1/3))) + ("Score: " + score).center(int(posx*1/3)))
        print()

   def afficher_les_cases(self, info_de_la_case, rows, col):#info_de_la_case = grid, module a appeler a la fin d'une action valide
        ligne_a_afficher = "" 
        #Boucle pour string des cases, une fois qu'on a la string il faut simplement la print(string) n fois pour faire la heuteur de la case
        for nb_rows in range(col): 
            for nb_col in range(rows):
                if (info_de_la_case[nb_rows][nb_col] == 'D'):
                    ligne_a_afficher += (("X"*self.largeur_case)+(" "*self.espace_entre_cases))

                elif (info_de_la_case[nb_rows][nb_col] == 'J'):
                    ligne_a_afficher += (("F"*self.largeur_case)+(" "*self.espace_entre_cases))

                elif (info_de_la_case[nb_rows][nb_col] == 'A'):
                    ligne_a_afficher += (("D"*self.largeur_case)+(" "*self.espace_entre_cases))

                elif (info_de_la_case[nb_rows][nb_col] == ' '):
                    ligne_a_afficher += (("C"*self.largeur_case)+(" "*self.espace_entre_cases))
                else:
                    None
            for i in range(3):
                #Ne pas oublier d'enlever le "  " a la fin des strings quand on affiche le jeu bien centrer ex: "CCCCC  CCCCC  " -> "CCCCC  CCCCC"
                print(ligne_a_afficher.center(get_terminal_size().columns - self.espace_entre_cases))
            print()
            ligne_a_afficher = "" #Ensuite la remettre a "" pour la deuxieme rangee de cases et ainsi de suite        

    def afficher_footer(self, sorte_de_teleporteur, nb_de_zap):    
        posx = get_terminal_size().columns 
        print( ("TELEPORTEUR (z) : " + sorte_de_teleporteur).center(int(posx*1/3)) + (" ").center(int(posx*1/3))+ ("ZAP (x): "+ "["+nb_de_zap+"]").center(int(posx*1/3)))
   
def show_game_view():
    liste_des_cases = GameGrid.GameGrid().grid
    row = GameGrid.GameGrid().rows
    col = GameGrid.GameGrid().column
    #les param de Game a renommer
    difficulte = Game.Game().difficulte
    niveau = Game.Game().niveau
    score = Game.Game().score
    sorte_de_teleporteur = Game.Game().sorte_de_teleporteur
    nb_de_zap = Game.Game().nb_de_zap

    GameView().afficher_header(difficulte, niveau, score)
    GameView().afficher_les_cases(liste_des_cases, row, col)
    GameView().afficher_footer(sorte_de_teleporteur, nb_de_zap)
