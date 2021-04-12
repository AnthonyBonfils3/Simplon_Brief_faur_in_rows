#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 02 10:25:37 2021

@author: bonfils
"""
from abc import ABC, abstractmethod
import numpy as np
import tensorflow as tf

Qlearning_model_path = './Qlearning/models/'

class Player(ABC): ## la classe doit être abstraite pour pouvoir utiliser
    ## une méthode abstraite (donc classe hérite de ABC)
    def __init__(self, board, name:str='player 1', couleur="Red"):
        """ 
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        self.board      = board 
        self.name       = name
        self.couleur    = couleur

        if self.couleur=="Red":
            self.value  = 1
        elif self.couleur=="Yellow":
            self.value  = -1
    
    @abstractmethod ## méthode abstraite doit être redéfinie dans les class filles
    def play(self):
        """
            -------------
            DESCRIPTION :   Choose a column to put a pawn
            -------------   
        """
        pass



class Human(Player):
    def __init__(self, board, name='Ia1', couleur="Red"):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        Player.__init__(self, board, name=name, couleur=couleur)
        print('---> Human initialized <---')


    def play(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        column = int(input(f"entrez la position d'une colonne (integer between 1 and {self.board.n_columns}: "))-1
        return column




class Ia(Player):
    def __init__(self, board, name='Ia1', couleur="Red", strategy='random', mode='1'):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        Player.__init__(self, board, name=name, couleur=couleur)
        self.strategy = strategy ## type d'IA -> random   q_learning 
        self.mode     = mode
        if self.strategy=='Q_learning':
            if self.mode==1:
                filepath = Qlearning_model_path + 'model_test.h5' # 'P4_model_train_rand_2000_step.h5'

            elif self.mode==2:
                filepath = Qlearning_model_path + 'model_qlearning195.h5' # 'model_qlearning100.h5'
                
            elif self.mode==3:
                filepath = Qlearning_model_path + 'model_qlearning500.h5' ## 'model_qlearning1.h5'

            elif self.mode==4:
                filepath = Qlearning_model_path + 'model_CNNqlearning40.h5'

            else:
                print(f"Error : strategy {self.strategy} with mode {self.mode} is not available yet.")
            
            self.model = tf.keras.models.load_model(filepath, custom_objects=None, compile=True, options=None)
        if  (self.strategy=='random'):
            print('---> Random IA initialized <---')
        elif (self.strategy=='Q_learning'):
            print('---> Q_learning IA initialized <---')

    def play(self):
        """
            -------------
            DESCRIPTION :   
            -------------
            INPUT :     self : 
            IOUTPUT :   
            -------------         
        """
        if (self.strategy=='random'):
            column = np.random.randint(0, self.board.n_columns)

        elif (self.strategy=='heuristics'):
            print(f"Error : strategy {self.strategy} is not available yet.")

        elif (self.strategy=='Q_learning'):
            if (self.mode==1):
                current_state_flat = self.board.grid.reshape(1,-1)
                column = np.argmax(self.model.predict(current_state_flat)[0])
                print("Qlearning model choice of column", column)

            elif (self.mode==2):
                current_state_flat = self.board.grid.reshape(1,-1)
                column = np.argmax(self.model.predict(current_state_flat)[0])
                print("Qlearning model choice of column", column)

            elif (self.mode==3):
                current_state_flat = self.board.grid.reshape(1,-1)
                column = np.argmax(self.model.predict(current_state_flat)[0])
                print("Qlearning model choice of column", column)

            elif (self.mode==4):
                current_state_reshape = np.reshape(self.board.grid, (1, self.board.n_rows, self.board.n_columns, 1))
                column = np.argmax(self.model.predict(current_state_reshape)[0])
                print("Qlearning model choice of column", column)


            else:
                print(f"Error : strategy {self.strategy} with mode {self.mode} is not available yet.")

        else:
            print(f"Error : strategy {self.strategy} is not available yet.")

        
        return column