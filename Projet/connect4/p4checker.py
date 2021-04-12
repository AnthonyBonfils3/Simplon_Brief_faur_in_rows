#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 08 10:59:55 2021

@author: bonfils
"""

import numpy as np

class Checker:
    def __init__(self, board, n_align_win=4):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        self.board          = board
        self.n_rows         = self.board.n_rows
        self.n_columns      = self.board.n_columns
        self.pawn_idx       = (-1, -1)
        self.idx_first_elmt = (-1, -1)
        self.n_align_win    = n_align_win
        self.win            = False


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
        return np.count_nonzero(self.board.grid[0, col])==1


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
        return np.count_nonzero(self.board.grid)==self.n_rows*self.n_columns


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
        inf_y              = max(0,-3+self.pawn_idx[1])
        sup_y              = min(self.pawn_idx[1]+4, self.n_columns)
        row_of_played_pawn = self.board.grid[self.pawn_idx[0], inf_y:sup_y]
        # print("selected row :", row_of_played_pawn)
        test_vector        = np.ones(self.n_align_win)
        conv               = np.convolve(row_of_played_pawn, test_vector)
        # print("convolution :", conv)

        if self.value*4 in conv:
            somm           = self.value*4 
            self.win       = True
            print("faur in row")
            ## attention il y a un probblème sur la determination de l'index lorsque la
            ## convolution ne commence pas toute à droite
            if self.value<0:
                self.idx_first_elmt = (self.pawn_idx[0], np.argmin(conv)-self.n_align_win+1)
            if self.value>0:
                self.idx_first_elmt = (self.pawn_idx[0], np.argmax(conv)-self.n_align_win+1)
                
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
        column_of_played_pawn   = self.board.grid[self.pawn_idx[0]:, self.pawn_idx[1]]
        # print("selected column :", column_of_played_pawn)
        
        test_vector             = np.ones(self.n_align_win)
        conv                    = np.convolve(column_of_played_pawn, test_vector)
        # print("convolution :", conv)

        if self.value*4 in conv:
            somm                = self.value*4 
            self.win            = True
            print("faur in columns")
            self.idx_first_elmt = self.pawn_idx

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
        symX = X.copy()
        n_columns = X.shape[1] 
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
            print("faur in diag")
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
            OUTPUT :        flag : (bool) -> True if four identic tokens are detected 
                                          -> else False 
                            somm :
            -------------         
        """
        symX = self.SysM(X)
        somm = self.faur_in_diag(symX)
        return somm  


    def verif(self, pawn_idx, value):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :         
            OUTPUT :        
            -------------         
        """
        self.pawn_idx = pawn_idx
        self.value = value
        ## vérif in rows
        somm       = self.faur_in_row()   
        
        ## vérif in columns
        somm       = self.faur_in_columns()

        ## vérif in diag and undiag
        list_tuple = []
        inf_x      = max(0, self.pawn_idx[1]-3)
        sup_x      = min(self.pawn_idx[1]+1, self.n_columns-3)
        inf_y      = max(0,-3+self.pawn_idx[0])
        sup_y      = min(self.n_rows-3, self.pawn_idx[0]+1)
        for i in range(inf_y, sup_y):
            for j in range(inf_x, sup_x):
                list_tuple.append((i,j))

        for i, j in list_tuple:
            sub_X  = self.board.grid[i:4+i, j:4+j]
            # print(sub_X)

            ## 4 in diag
            somm   = self.faur_in_diag(sub_X)

            ## 4 in undiag
            somm   = self.faur_in_undiag(sub_X)

