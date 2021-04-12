#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 09 12:31:16 2021

@author: bonfils
"""
import os
curent_path = os.getcwd()
curent_path = os.path.realpath('test_class_board.py')[:-19]
print(curent_path)
import sys
sys.path.append("connect4") ## ou ../connect4 si on se trouve dans le répertoire de test
from board import Board
import pytest

class TestBoard:
    n_rows = 6
    n_columns = 7
    board = Board()
    def test_generate_board(generate_board):
        pass
