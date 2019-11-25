# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:16:17 2018

@author: duxiaoqin

Functions:
    (1) TTTDraw class;
"""

from graphics import *
from tictactoe import *
from tttinput import *

class TTTDraw:
    WIDTH = 5.0
    HEIGHT = 5.0
    START = 1.0
    END = 4.0
    
    def __init__(self, win):
        self.win = win
        self.win.setCoords(0.0, 0.0, TTTDraw.WIDTH, TTTDraw.HEIGHT)
        
        self.lines = []
        for offset in range(4):
            l = Line(Point(TTTDraw.START, TTTDraw.START+offset), \
                     Point(TTTDraw.END, TTTDraw.START+offset))
            l.setWidth(3)
            self.lines.append(l)
            l = Line(Point(TTTDraw.START+offset, TTTDraw.START), \
                     Point(TTTDraw.START+offset, TTTDraw.END))
            l.setWidth(3)
            self.lines.append(l)
            
        self.ximg = Image(Point(0, 0), 'x.gif')
        self.oimg = Image(Point(0, 0), 'o.gif')
        
        self.ximgs = Array2D(3, 3)
        for row in range(3):
            for col in range(3):
                newximg = self.ximg.clone()
                newximg.move(TTTDraw.START+1/2+col, TTTDraw.END-1/2-row)
                self.ximgs[row, col] = newximg
        self.oimgs = Array2D(3, 3)
        for row in range(3):
            for col in range(3):
                newoimg = self.oimg.clone()
                newoimg.move(TTTDraw.START+1/2+col, TTTDraw.END-1/2-row)
                self.oimgs[row, col] = newoimg
        
        self.text = Text(Point(2.5, 0.5), '')
        self.text.setTextColor('red')
        
    def draw_lines(self):
        for l in self.lines:
            l.undraw()
        for l in self.lines:
            l.draw(self.win)
            
    def draw_ttt(self, ttt):
        self.text.undraw()
        if ttt.isGameOver() == TicTacToe.BLACKWIN:
            self.text.setText('X Win')
        elif ttt.isGameOver() == TicTacToe.WHITEWIN:
            self.text.setText('O Win')
        elif ttt.isGameOver() == TicTacToe.DRAW:
            self.text.setText('X/O Draw')
        elif ttt.getPlayer() == TicTacToe.BLACK:
            self.text.setText('X to play')
        elif ttt.getPlayer() == TicTacToe.WHITE:
            self.text.setText('O to play')
        self.text.draw(self.win)

        for row in range(3):
            for col in range(3):
                self.ximgs[row, col].undraw()
                self.oimgs[row, col].undraw()
                
        for row in range(3):
            for col in range(3):
                if ttt.board[row, col] == TicTacToe.BLACK:
                    self.ximgs[row, col].draw(self.win)
                elif ttt.board[row, col] == TicTacToe.WHITE:
                    self.oimgs[row, col].draw(self.win)
                    
    def draw(self, ttt):
        self.draw_lines()
        self.draw_ttt(ttt)    
        self.win.update()
            
def main():
    win = GraphWin('TTTDraw', 600, 600, autoflush=False)
    ttt = TicTacToe()
    tttdraw = TTTDraw(win)
    tttinput = TTTInput(win)

    while win.checkKey() != 'Escape':
        tttinput.input(ttt)
        tttdraw.draw(ttt)
        if ttt.isGameOver() != None:
            ttt.reset()
            win.getMouse()
    win.close()
    
if __name__ == '__main__':
    main()