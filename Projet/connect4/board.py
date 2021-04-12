#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 08 11:01:42 2021

@author: bonfils
"""

import numpy as np
import pandas as pd

class Board:
    def __init__(self, n_rows=6, n_columns=7):   
        """
            -------------
            DESCRIPTION :   Init of the board. Take the dimension and create the
                            grid (numpy array - dimension n_rows * n_columns)
            -------------
            INPUT :         self
                            n_rows    : desired number of rows 
                            n_columns : desired number of columns    

            OUTPUT :        grid
            -------------         
        """
        self.n_rows    = n_rows
        self.n_columns = n_columns

        ## Generate the board
        self.generate_board()


    def generate_board(self):     
        """
            -------------
            DESCRIPTION :   Create a empty board (n_rows * n_columns)
            -------------
            INPUT :         self : 
            OUTPUT :        board : (np-2d arrays) -> squared Matrix (n_rows * n_columns)
            -------------         
        """
        self.grid = np.zeros((self.n_rows, self.n_columns), dtype=int)


    def show_board(self):
        """
            -------------
            DESCRIPTION :   Create a DataFrame with the grid to show it in
                            terminal
            -------------
            INPUT :         self : object (need the board)
            OUTPUT :        board_df : DataFrame using the board.
                            Columns and rows are numbered from 1 to n_columns, 
                            respectively n_rows 
            -------------         
        """
        columns  = np.array([i for i in range(1, 8)])
        indices  = np.array([i for i in range(1, 7)])
        board_df = pd.DataFrame(self.grid, columns=columns, index=indices)
        print(board_df)