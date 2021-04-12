#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 02 10:25:37 2021

@author: bonfils
"""

## Imports
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod ## pour créer des classes et méthodes abstraites

import tkinter as tk
import sys
import os
from tkinter import NW, Label, Button

### Local Class
from player import Ia, Human
from board import Board
from p4checker import Checker
from Qlearning.autre_fcn import clear

clear()

#####################################################################
#######################                  ############################
#######################     Connect4     ############################
#######################                  ############################
#####################################################################

class Connect4(ABC): 
    def __init__(self, n_rows=6, n_columns=7, n_align_win=4, game_type='HumanVsHuman', strategy='random', mode=1):     
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            OUTPUT :   
            -------------         
        """
        ## init board
        self.n_rows         = n_rows
        self.n_columns      = n_columns
        self.is_valid_n_rows()
        self.is_valid_n_columns()
        self.board          = Board(self.n_rows, self.n_columns)

        ## init checker
        self.n_align_win    = n_align_win
        self.checker        = Checker(self.board, self.n_align_win)

        ## variables
        self.game_type      = game_type
        self.strategy       = strategy
        self.mode           = mode
        self.n_player       = 1         ## index of player
        self.pawn_idx       = (-1, -1)
        self.win            = False

        ## init value to add
        self.posible_values = [-1, 1]  ## [-1, 1]  or   [1, -1] 
        self.value          = self.posible_values[1]

        if self.game_type == 'HumanVsHuman':
            ## initialize players
            self.player1 = Human(self.board, name="player 1", couleur="Red")
            self.player2 = Human(self.board, name="player 2", couleur="Yellow")

        elif self.game_type == 'HumanVsIa':
            ## initialize players
            self.player1 = Human(self.board, name="player", couleur="Red")
            self.player2 = Ia(self.board, name="IA", couleur="Yellow", strategy=self.strategy, mode=self.mode)

        elif self.game_type == 'IaVsIa':
            ## initialize players
            self.player1 = Ia(self.board, name="IA 1", couleur="Red", strategy=self.strategy, mode=self.mode)
            self.player2 = Ia(self.board, name="IA 2", couleur="Yellow", strategy=self.strategy, mode=self.mode)

        else:
            print("Error : Non valid game_type")

    
    def is_valid_n_rows(self):
        """
            -------------
            DESCRIPTION :   Testing if n_rows value is available. Raise 
                            an error if n_rows is not an integer or 
                            négative
            ------------- 
        """
        if (type(self.n_rows)!=int):
            raise TypeError("Number of rows must be an integer")

        if (self.n_rows<0):
            raise ValueError("Number of rows is not positive")

    
    def is_valid_n_columns(self):
        """
            -------------
            DESCRIPTION :   Testing if n_rows value is available. Raise 
                            an error if n_rows is not an integer or 
                            négative
            ------------- 
        """
        if (type(self.n_columns)!=int):
            raise TypeError("Number of rows must be an integer")

        if (self.n_columns<0):
            raise ValueError("Number of rows is not positive")
        

    def reset(self):  
        """
            -------------
            DESCRIPTION :   Reset the Game by calling __init__() method
            -------------
        """
        self.__init__()


    def change_player(self):
        """
            -------------
            DESCRIPTION :   Permute players when called
            -------------  
        """
        ## value to add
        self.n_player = [0, 1][[0, 1].index(self.n_player)-1] ## permutation of players
        self.value  = self.posible_values[self.n_player]
        self.pawn_added = False


    def add_pawn(self, col, row=0):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            OUTPUT :   
            -------------         
        """
        self.pawn_added = False
        if self.checker.is_bord_full():
            print("----"*15)
            print("board plein -> quit the game")
            print("----"*15)

        elif self.checker.is_column_full(col):
            print("----"*15)
            print("colonne pleine -> entrez une autre valeur")
            print("----"*15)

        else:
            if row==5:
                self.board.grid[row, col] = self.value
                self.pawn_added = True
                self.pawn_idx = (row, col)
            else:
                if self.board.grid[row+1, col]==0:
                    self.add_pawn(col, row+1)
                else:
                    self.board.grid[row, col] = self.value
                    self.pawn_added = True
                    self.pawn_idx = (row, col)


    @abstractmethod
    def play_game(self):
        """
            -------------
            DESCRIPTION :   Abstract method --> defined in herited classes
            -------------
        """
        pass



#####################################################################
#######################                  ############################
#######################   On Terminal    ############################
#######################                  ############################
#####################################################################
class Connect4OnTerminal(Connect4):
    def __init__(self, n_rows=6, n_columns=7, n_align_win=4, game_type='HumanVsHuman', strategy='random', mode=1):     
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        print("Start game Connect faur, interface --> terminal")
        Connect4.__init__(self, n_rows=n_rows, n_columns=n_columns, n_align_win=4, game_type=game_type, strategy=strategy, mode=mode)


    def play_game(self):
        """
            -------------
            DESCRIPTION :   Play a Connect 4 game with terminal interface
            -------------
            INPUT :         self 
            -------------         
        """
        while self.checker.is_bord_full()==False:
            try:
                if self.n_player==0:
                    col_value = self.player2.play()
                elif self.n_player==1:
                    col_value = self.player1.play()
                else:
                    print("Error : Invalid number of player")

            except ValueError:
                print("Warning column choice must be an integer")
            finally:
                if col_value>=0 and col_value<=6:
                    self.add_pawn(col_value)
                    print(self.pawn_added)
                    if self.pawn_added:
                        print(self.pawn_idx)
                        self.checker.verif(pawn_idx=self.pawn_idx, value= self.value)
                        self.board.show_board()
                        if self.checker.win:
                            print(f"Player {self.posible_values[self.n_player]} win -> END of the game")
                            break
                        self.change_player()
                else:
                    print("Warning column choice must be an integer between 1 and 7")

        ## If nobody won the game          
        if self.checker.is_bord_full():    
            print("Fin de la partie --> MATCH NUL")



#####################################################################
#######################                   ###########################
#######################   with tkinter    ###########################
#######################                   ###########################
#####################################################################
class Connect4DisplayTkinter(Connect4):
    def __init__(self, n_rows=6, n_columns=7, game_type='HumanVsHuman', n_align_win=4):     
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        print("Start game Connect faur, interface --> tkinter")
        Connect4.__init__(self, n_rows=n_rows, n_columns=n_columns, n_align_win=4, game_type=game_type, strategy=strategy, mode=mode)


    def play_game(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        pass



#####################################################################
#####################################################################
#######################                  ############################
#######################       MAIN       ############################
#######################                  ############################
#####################################################################
#####################################################################
def main():
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')
        
    ## Choice for n_rows and n_columns
    n_rows       = 6
    n_columns    = 7

    ## Game type choice
    question     = ""
    while question!="HumanVsHuman" and question!="HumanVsIa" and question!="IaVsIa":
        question = input("Type of game : HumanVsHuman, HumanVsIa, IaVsIa? ")

    game_type    = question  ## IaVsIa  ## HumanVsIa  ## HumanVsHuman

    ## IA type choice if party is HumanVsIa game or IaVsIa game
    if game_type=="HumanVsIa" or game_type=="IaVsIa":
        while question!="random" and question!="Q_learning" and question!="heuristics":
            question = input("Type of IA: random, Q_learning, heuristics? ")

    strategy     = question    ## Q_learning
    mode         = 1

    ## Interface 

    ## initialize game
    game         = Connect4OnTerminal(n_rows=n_rows, n_columns=n_columns, 
                        game_type = game_type, strategy = strategy, mode=mode)
    game.board.show_board()

    ## Play a party
    game.play_game()

if __name__=='__main__':
    main()

 