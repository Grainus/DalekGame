from os import get_terminal_size, system
from game import Game

class GameView:
    # Il faut game.player.score game.player.name de Game  
    def __init__(self, game : Game):
        self.game = game
        self.espace_entre_cases = int(get_terminal_size().columns * 1/50)
        self.espace_entre_casesy =  int(get_terminal_size().lines * 1/20)
        self.largeur_case  = int(get_terminal_size().columns * 1/30)
        self.hauteur_case  = int(get_terminal_size().columns * 1/55)

    def afficher_header(self, niveau, score):
        if (self.game.difficulty == 0):
            difficulte = "Facile"
        if (self.game.difficulty == 1):
            difficulte = "Moyen"
        if (self.game.difficulty == 2):
            difficulte = "Difficile"

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
            for i in range(self.hauteur_case):
                #Ne pas oublier d'enlever le "  " a la fin des strings quand on affiche le jeu bien centrer ex: "CCCCC  CCCCC  " -> "CCCCC  CCCCC"
                print(ligne_a_afficher.center(get_terminal_size().columns - self.espace_entre_cases))
            for j in range(self.espace_entre_casesy):
                print("")
            ligne_a_afficher = "" #Ensuite la remettre a "" pour la deuxieme rangee de cases et ainsi de suite    

    def afficher_footer(self, difficulte, nb_de_zap): 
        if (difficulte == 0):
            sorte_de_teleporteur = "Securitaire"
        if (difficulte == 1):
            sorte_de_teleporteur = "Normale"
        if (difficulte == 2):   
            sorte_de_teleporteur = "Dangereux"
        posx = get_terminal_size().columns 
        print( ("TELEPORTEUR (z) : " + sorte_de_teleporteur).center(int(posx*1/3)) + (" ").center(int(posx*1/3))+ 
        ("ZAP (x): "+ "["+nb_de_zap+"]").center(int(posx*1/3))+"\n")

    def show_game_view(self):

        liste_des_cases = self.game.grid
        row = self.game.grid.width
        col = self.game.grid.height
        #les param de Game a renommer
        difficulte = self.game.difficulty
        niveau = self.game.niveau
        score = self.game.score
        nb_de_zap = self.game.doctor.zap_count
        system('cls')
        GameView().afficher_header(niveau, score)
        GameView().afficher_les_cases(liste_des_cases, row, col)
        GameView().afficher_footer(difficulte, nb_de_zap)
