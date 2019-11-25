# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 19:13:37 2018

@author: duxiaoqin

Functions:
    (1) TTTInput class;
"""

from graphics import *
from tictactoe import *

class TTTInput:
    def __init__(self, win):
        self.win = win
        
    def input(self, ttt):
        mpos = self.win.checkMouse()
        if mpos == None:
            return False
        moves = ttt.getAllMoves()
        row, col = 4-int(mpos.getY())-1, int(mpos.getX())-1
        if (row, col) not in moves:
            return False
        ttt.play(row, col)
        return True