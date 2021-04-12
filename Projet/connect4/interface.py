#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 02 10:25:37 2021

@author: bonfils
"""

## Imports lib
import tkinter as tk
import sys
import os
from tkinter import NW, Label, Button

### Local Class
from board import Board
from Qlearning.autre_fcn import clear

clear()


class Can(tk.Canvas):

    def __init__(self, board):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        
            #Variables
        # self.cases      = [] # Cases déjà remplies
        # self.listerouge = [] # Liste des cases rouges
        # self.listejaune = [] # Liste des cases jaunes
        # self.dgagnantes = [] # Cases déjà gagnantes et donc ne peuvent plus l'être à nouveau (cf "Continuer")
        self.running    = 1  # Type de partie en cours -> normal ou continue
        self.mode = 1 ## 1 : HumanVsIa       2 : HumanVsHuman      3 : IaVsIa
        self.couleur    = ["Rouges", "Jaunes"]
        self.color      = ["red", "#EDEF3A"]
        self.board      = board
        self.n_rows     = self.board.n_rows
        self.n_columns  = self.board.n_columns

            ### dimension
        self.padding_left = 10
        self.padding_right = 10
        self.padding_top = 10
        self.padding_bottom = 10
        self.x_rectangle = 95 ## largeur rectangle clicable
        self.y_rectangle = 25 ## hauteur rectangle clicable
        self.diam_cercles = 50
        self.len_x_cercles = (self.n_columns)*self.diam_cercles+(self.n_columns-1)*13 ## dim n cercles espacé de 13 px
        self.width = self.len_x_cercles + self.padding_left + self.padding_right ## fen width = width for cercles + 10 px each side
        self.len_y_cercles = (self.n_rows)*self.diam_cercles + (self.n_rows-1)*5
        self.height = self.padding_top  + self.len_y_cercles + self.padding_bottom + 35 ## fen height = height for cercles + 10 px top and 30 px below

            #Interface
        self.clair      = "light blue"
        self.fonce      = "navy blue"
        self.police1    = "Times 17 normal"
        self.police2    = "Arial 10 normal"
        self.police3    = "Times 15 bold"
        tk.Canvas.__init__(self, 
                                width =self.width , 
                                height = self.height, 
                                bg=self.fonce, bd=0)
        self.relief     = 'raised'
        
        # self.grid(row = 1, columnspan = 5)

            # Joueur en cours
        self.joueur = 1
        self.create_rectangle(self.padding_left, 
                            self.height-35, 
                            self.padding_left+self.x_rectangle, 
                            self.height-self.padding_bottom, 
                            fill = self.clair)
        self.create_text(self.padding_left+10, 
                            self.height-30, text ="Player :", 
                            anchor = NW, fill = self.fonce, font= self.police2)
        self.indiccoul = self.create_oval(85, self.height-30, 100, self.height-15, fill = self.color[1])
        
            #Bouton Nouveau Jeu
        self.create_rectangle(self.width-self.x_rectangle-self.padding_right,
                            self.height-35,
                            self.width-self.padding_right,
                            self.height-self.padding_bottom, 
                            fill=self.clair)
        self.create_text(self.width-self.padding_right-self.x_rectangle+20, 
                            self.height-30, text ="New game", anchor = NW, 
                            fill = self.fonce, font= self.police2)
        
            #Création des cases
        self.ovals = []
        for y in range(self.padding_top, self.padding_top+\
                        self.diam_cercles*self.n_rows-5, 55):
            for x in range(self.padding_left, self.width-5, 63):
                self.ovals.append(self.create_oval(x, y, x + self.diam_cercles, y + self.diam_cercles , fill= "white"))
        print(self.ovals) 

            #En cas de click  
        self.bind("<Button-1>", self.click)
        
            # Pour relier à la fin les coordonnées des centres des cases
        self.coordscentres = []
        
        #     # Dictionnaire de reconnaissance
        # self.dictionnaire = {}
        # v = 0
        # for y in range(self.padding_top, self.padding_top+\
        #                 self.diam_cercles*self.n_rows-5, 55):
        #     for x in range(self.padding_left, self.width-5, 63):
        #         self.dictionnaire[(x, y, x + self.diam_cercles, y + self.diam_cercles)] = v
        #         v += 1
        #         self.coordscentres.append((x + self.diam_cercles/2, y + self.diam_cercles/2))


    def _position_x_to_column(self, x, y):
        """Donne l'identifiant de la colonne en fonction de la position du click"""
        col = -1
        if y>self.padding_top and y<self.padding_top+self.len_y_cercles:
            for i in range(self.n_columns):
                if x>self.padding_left+i*63 and x<self.padding_left+i*63+self.diam_cercles:
                    col = i+1
                    break
        return col


    def _column_to_position_x(self, id):
        """Réciproque de la fonction précédente"""
        return (id % self.n, id // self.n)


    def click(self, event): #En cas de click
        if self.width-self.x_rectangle-self.padding_right < event.x and self.height-35 < event.y and event.x < self.width-self.padding_right and event.y < self.height-self.padding_bottom:
            self.new()# =>Nouveau jeu
            
            #Jeu en cours: reconnaissance de la case jouée
        else:
            col = self._position_x_to_column(event.x, event.y)
            print(f"we click on column {col}")


    def new(self):# Nouveau Jeu
            
            # Opérations certaines
        self.destroy()
        self.__init__(self.board)



#####################################################################
#######################                  ############################
#######################       MAIN       ############################
#######################                  ############################
#####################################################################
def main():
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    #create main window
    window = tk.Tk()
    window.title("Puissance 4 -- by Anthony")
    window.config(bg="navy blue")




    # Configuration du gestionnaire de grille
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    ## Inputs for game dimensions  "TEST"
    value_n_rows = tk.StringVar(window)
    value_n_rows.set("Nb of rows")
    
    entree_n_rows = tk.Entry(window, textvariable=value_n_rows, width=10)
    # Placement du bouton dans «root»
    entree_n_rows.grid(row=0, column=0, columnspan=1)#, sticky='ew')
    # entree.pack()
    
    #On lie la fonction à l'Entry
    #La fonction sera exécutée à chaque fois que l'utilisateur appuie sur "Entrée"
    # entree_n_rows.bind("<Return>", print_name)

    # val = entree_n_rows.bind("<Return>", get_n_rows)
    # print(val)

    def get_n_rows():
        res = entree_n_rows.get()
        print(res)

    btn = tk.Button(window, height=1, width=10, text="Ok", command=get_n_rows).grid(row=0, column=1, columnspan=1)
    

    ###############################################
    ## Inputs for game dimensions  "TEST"
    value_n_cols = tk.StringVar(window)
    value_n_cols.set("Nb of columns")
    
    entree_n_cols = tk.Entry(window, textvariable=value_n_cols, width=10)
    # Placement du bouton dans «root»
    entree_n_cols.grid(row=0, column=2, columnspan=1)
    # entree.pack()

    # val = entree_n_cols.bind("<Return>", get_n)
    # print(val)

    def get_n_cols():
        res = entree_n_cols.get()
        print(res)
    
    btn = tk.Button(window, height=1, width=10, text="Ok", command=get_n_cols).grid(row=0, column=3, columnspan=1)
    



    ## Create the board
    # ## n_rows=6, n_columns=7 par défaut pas obligatioire ## n_rows=8, n_columns=10
    n_rows    = 6
    n_columns = 7
    board     = Board(n_rows=n_rows, n_columns=n_columns)

    ## Create a new Canevas
    # lecan = Can(board)
    lecan = Can(board).grid(row = 1, columnspan = 4)

    # Run forever!
    window.mainloop()   

if __name__ ==	"__main__" :
    main()

