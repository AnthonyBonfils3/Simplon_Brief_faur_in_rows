#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 06 10:25:37 2021

@author: bonfils
"""

## Imports
import numpy as np
import pandas as pd
from autre_fcn import clear

clear()

#####################################################################
#######################                  ############################
#######################     Connect4     ############################
#######################                  ############################
#####################################################################
class Connect4:
    def __init__(self, n_rows=6, n_columns=7, n_align_win=4):     
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            OUTPUT :   
            -------------         
        """
        ## variables
        self.n_rows         = n_rows
        self.n_columns      = n_columns
        self.observ_shape   = (n_rows, n_columns)
        self.n_action_space = n_columns
        self.n_align_win    = n_align_win
        self.player         = 1
        self.nb_total_pawns = 42
        self.played_pawns   = 0
        self.idx            = (-1, -1)
        self.idx_first_elmt = (-1, -1)
        self.win            = False

        ## init board
        self.board          = self.generate_board()

        ## init value to add
        self.posible_values = [-1, 1] ## [-1, 1]  or   [1, -1] 
        self.value          = self.posible_values[1]


    def generate_board(self):     
        """
            -------------
            DESCRIPTION :   Create a empty board (n_rows * n_columns)
            -------------
            INPUT :         self : 
            OUTPUT :        board : (np-2d arrays) -> squared Matrix (n_rows * n_columns)
            -------------         
        """
        board = np.zeros((self.n_rows, self.n_columns), dtype=int)
        return board


    def reset(self):  
        """
            -------------
            DESCRIPTION :   Create a empty board (n_rows * n_columns)
            -------------
            INPUT :         self : 
            OUTPUT :        board : (np-2d arrays) -> squared Matrix (n_rows * n_columns)
            -------------         
        """
        return self.__init__()


    def show_board(self):
        """
            -------------
            DESCRIPTION :   Create a DataFrame with the grig to show in terminal
            -------------
            INPUT :         self : object (need the board)
            OUTPUT :        board_df : DataFrame using the board.
                            Columns and rows are numbered from 1 to n_columns, 
                            respectively n_rows 
            -------------         
        """
        ## decale columns and row from the indices
        # columns = np.array([i for i in range(1, self.n_columns+1)])
        # indices = np.array([i for i in range(1, self.n_rows+1)])


        ## columns and row like the indices
        columns = np.array([i for i in range(0, self.n_columns)])
        indices = np.array([i for i in range(0, self.n_rows)])
        board_df = pd.DataFrame(self.board, columns=columns, index=indices)
        return board_df


    def change_player(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            OUTPUT :   
            -------------         
        """
        ## value to add
        self.player = [0, 1][[0, 1].index(self.player)-1] ## permutation of players
        self.value  = self.posible_values[self.player]
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
        if self.is_bord_full():
            print("----"*15)
            print("board plein -> quit the game")
            print("----"*15)

        elif self.is_column_full(col):
            print("----"*15)
            print("colonne pleine -> entrez une autre valeur")
            print("----"*15)

        else:
            if row==5:
                self.board[row, col]     = self.value
                self.pawn_added         = True
                self.idx                = (row, col)
            else:
                if self.board[row+1, col]==0:
                    self.add_pawn(col, row+1)
                else:
                    self.board[row, col] = self.value
                    self.pawn_added     = True
                    self.idx            = (row, col)


    def is_column_full(self, col):
        """
            -------------
            DESCRIPTION :   Detect if the choice column is full
            -------------
            INPUT :         self  
            OUTPUT :        Bool -> True, if the column is full
                                    False, either
            -------------         
        """
        # print("column full", np.count_nonzero(self.board[0, col])==1)
        return np.count_nonzero(self.board[0, col])==1


    def is_bord_full(self):
        """
            -------------
            DESCRIPTION :   Detect if the board is full
            -------------
            INPUT :         self  
            OUTPUT :        Bool -> True, if the board is full
                                    False, either
            -------------         
        """
        # print("board full", np.count_nonzero(self.board)==self.n_rows*self.n_columns)
        return np.count_nonzero(self.board)==self.n_rows*self.n_columns



    def step(self, a, strategy='random'):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :         self
                            a      -> action : column for Agent add a pawn

            OUTPUT :        board  : for the next step 
                                    (np 2D-array : n_rows * n_columns)

                            reward : -> 1 :     if the agent wins
                                     -> -1:     if the adversal player wins
                                     -> 0 :     either

                            done   : -> True    if someone win
                                     -> False   either
            -------------         
        """
        ##########################
        ########  Agent  #########
        ##########################
        ## modify the current state with the action a
        self.add_pawn(a)
        if not self.pawn_added:
            if self.is_column_full(a): ## cas particulier l'agent ne joue pas car la colonne est full
                return -1
            elif self.is_bord_full(): ## cas particulier l'agent ne joue pas car la bord est full
                return self.board, 0, True

        ## test P4 in the board
        self.verif()
        ## if action leads to win
        if self.win: 
            return self.board, 1, True
            
        ##########################
        ####  Adverse Player  ####
        ##########################
        ## Cahnge player
        self.change_player()

        ## modify the state with the pawn of adversal player 
        ## if the board is not full while the adversal player
        ## add not found a non full column
        while not self.pawn_added:
            if not self.is_bord_full():
                if strategy=='random':
                    random_col = np.random.randint(0,7)
                    # print("Adevrse choice :", random_col)
                self.add_pawn(random_col)
            else:
                return self.board, 0, True

        ## test P4 in the board
        self.verif()
        ## if action leads to win
        if self.win: 
            return self.board, -1, True

        ##########################
        ## If nobody win -> Quit the step (Game terminated or not : with self.is_bord_full())
        return self.board, 0, self.is_bord_full()


    def faur_in_row(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :         
            OUTPUT :        
            -------------         
        """
        flag               = False
        somm               = 0
        row_of_played_pawn = self.board[self.idx[0], max(0,-3+self.idx[1]):min(self.idx[1]+4, self.n_columns)]
        # print("selected row :", row_of_played_pawn)
        test_vector        = np.ones(self.n_align_win)
        conv               = np.convolve(row_of_played_pawn, test_vector)
        # print("convolution :", conv)

        if self.value*4 in conv:
            somm           = self.value*4 
            self.win       = True
            print(f"faur {self.value} in row")
            ## attention il y a un probblème sur la determination de l'index lorsque la
            ## convolution ne commence pas toute à droite
            if self.value<0:
                self.idx_first_elmt = (self.idx[0], np.argmin(conv)-self.n_align_win+1)
            if self.value>0:
                self.idx_first_elmt = (self.idx[0], np.argmax(conv)-self.n_align_win+1)
                
        return somm    


    def faur_in_columns(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :         
            OUTPUT :        
            -------------         
        """
        flag                    = False
        somm                    = 0
        column_of_played_pawn   = self.board[self.idx[0]:, self.idx[1]]
        # print("selected column :", column_of_played_pawn)
        
        test_vector             = np.ones(self.n_align_win)
        conv                    = np.convolve(column_of_played_pawn, test_vector)
        # print("convolution :", conv)

        if self.value*4 in conv:
            somm                = self.value*4 
            self.win            = True
            print(f"faur {self.value} in columns")
            self.idx_first_elmt = self.idx

        return somm       

    def SysM(self, X):
        """
            -------------
            DESCRIPTION :   Permute columns of the square matrix X as a central
                            axial symmetry in the middle of X.
            -------------
            INPUT :         X : (np-2d arrays) -> squared Matrix (n*n)
            OUTPUT :        symX : squared Matrix (n*n) with permuted columns
            -------------         
        """
        # print(X)
        symX          = X.copy()
        n_columns     = X.shape[1] 
        for i in range(n_columns):
            symX[:,i] = X[:,-(i+1)]
        return symX


    def faur_in_diag(self, X):
        """
            -------------
            DESCRIPTION :   Determine if the matrix (X) digonal has 4 consecutives 
                            token exists. The sum of diagonal elements is computed using 
                            numpy trace fonction
            -------------
            INPUT :         X : (np-2d arrays) -> squared Matrix (n*n)
            OUTPUT :        flag : (bool) -> True if four identic tokens are detected 
                                          -> else False 
                            somm :
            -------------         
        """
        flag         = False
        somm         = np.trace(X)
        if somm==4*self.value:
            self.win = True
            print(f"faur {self.value} in diag")
        return somm  


    def faur_in_undiag(self, X):
        """
            -------------
            DESCRIPTION :   Determine if the matrix (X) digonal has 4 consecutives 
                            token exists. The columns are permuted using SysM fonction 
                            and the sum of diagonal elements is computed using 
                            numpy trace fonction
            -------------
            INPUT :         X : (np-2d arrays) -> squared Matrix (n*n)
            OUTPUT :        flag : (bool) - True if four identic tokens are detected 
                                          - else False 
                            somm :
            -------------         
        """
        symX = self.SysM(X)
        somm = self.faur_in_diag(symX)
        return somm  


    def verif(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :         
            OUTPUT :        
            -------------         
        """
        ## vérif in rows
        somm         = self.faur_in_row()   
        
        ## vérif in columns
        somm         = self.faur_in_columns()

        ## vérif in diag and undiag
        list_tuple   = []
        inf_x        = max(0, self.idx[1]-3)
        sup_x        = min(self.idx[1]+1, self.n_columns-3)
        inf_y        = max(0,-3+self.idx[0])
        sup_y        = min(self.n_rows-3, self.idx[0]+1)
        for i in range(inf_y, sup_y):
            for j in range(inf_x, sup_x):
                list_tuple.append((i,j))

        for i, j in list_tuple:
            sub_X    = self.board[i:4+i, j:4+j]
            # print(sub_X)

            ## 4 in diag
            somm     = self.faur_in_diag(sub_X)

            ## 4 in undiag
            somm     = self.faur_in_undiag(sub_X)



#####################################################################
#####################################################################
#######################                  ############################
#######################       MAIN       ############################
#######################                  ############################
#####################################################################
#####################################################################
if __name__=='__main__':
    ## Choice for n_rows and n_columns
    n_rows        = 6
    n_columns     = 7


    ## initialize game
    game          = Connect4(n_rows=n_rows, n_columns=n_columns)

    ## print the results
    board_df      = game.show_board()
    print(board_df)

    while not game.is_bord_full():
        a         = np.random.randint(0,7)
        print("----"*20)
        print("a =", a)

        ## call the step function
        next_step = game.step(a)

        ## print the results 
        print(next_step)
        # board_df   = game.show_board()
        # print(board_df)