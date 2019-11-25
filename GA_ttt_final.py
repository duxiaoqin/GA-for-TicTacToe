# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 21:23:04 2018

@author: duxiaoqin
Functions:
    (1) GA for TicTacToe, evolving a perfect strategy which never loses a game.
"""

from graphics import *
from tictactoe import *
from tttdraw import *
from tttinput import *
import sys
import time
from random import *
import numpy as np
import matplotlib.pyplot as plt
import pickle
import copy

EQUIVALENT = [
             [0,1,2,3,4,5,6,7,8],
             [6,3,0,7,4,1,8,5,2],
             [8,7,6,5,4,3,2,1,0],
             [2,5,8,1,4,7,0,3,6],
             [6,7,8,3,4,5,0,1,2],
             [8,5,2,7,4,1,6,3,0],
             [2,1,0,5,4,3,8,7,6],
             [0,3,6,1,4,7,2,5,8]]
generation_num = 3000
population_num = 800
prob_crossover = 0.15
prob_replicate = 0.10
prob_mutation = 0.001
INDIVIDUAL_TEMPLATE = {}
STATE = {}
POPULATION = []
FITNESS = [0]*population_num
PROB = [0]*population_num
T = range(generation_num)
BEST_FITNESS = [1]*generation_num
MAX_FITNESS = [0]*generation_num
AVERAGE_FITNESS = [0]*generation_num
MAX_INDIVIDUAL = [0]*generation_num

def GenEquivalent(ttt_str):
    TTT_STR = []
    for index in EQUIVALENT:
        TTT_STR.append(''.join([ttt_str[i] for i in index]))
    return TTT_STR

def GenEquivalentMove(base_str, base_move, equ_str):
    TTT_STR = GenEquivalent(base_str)
    move = base_move[0]*3+base_move[1]
    equ_index = TTT_STR.index(equ_str)
    move_index = EQUIVALENT[equ_index].index(move)
    return (move_index // 3, move_index % 3)

def Init():
    global INDIVIDUAL_TEMPLATE, STATE
    try:
        template_file = open('IndividualTemplate.dat', 'rb')
        INDIVIDUAL_TEMPLATE = pickle.load(template_file)
        template_file.close()
        
        state_file = open('State.dat', 'rb')
        STATE = pickle.load(state_file)
        state_file.close()
    except FileNotFoundError:
        INDIVIDUAL_TEMPLATE = {}
        STATE = {}
        ttt = TicTacToe()
        GenerateIndividualTemplate(ttt)
        
        template_file = open('IndividualTemplate.dat', 'wb')
        pickle.dump(INDIVIDUAL_TEMPLATE, template_file)
        template_file.close()
        
        state_file = open('State.dat', 'wb')
        pickle.dump(STATE, state_file)
        state_file.close()
        
    items = INDIVIDUAL_TEMPLATE.items()
    print(len(items))
    for i in range(population_num):
        individual = GenRandomIndividual(items)
        POPULATION.append(individual)
    fitness_sum = CalculateFitness()
    PROB[0] = FITNESS[0]/fitness_sum
    for i in range(1, len(FITNESS)):
        PROB[i] = PROB[i-1]+FITNESS[i]/fitness_sum

def GenerateIndividualTemplate(ttt):
    if ttt.isGameOver() != None:
        return
    
    moves = ttt.getAllMoves()
    ttt_str = ttt.ToString()
    if STATE.get(ttt_str) == None:
        for equ_str in GenEquivalent(ttt_str):
            STATE[equ_str] = ttt_str #base state
        INDIVIDUAL_TEMPLATE[ttt_str] = moves
    for move in moves:
        node = ttt.clone()
        node.play(*move)
        GenerateIndividualTemplate(node)
    
def GenRandomIndividual(items):
    seed()
    individual = {}
    for ttt_str, moves in items:
        individual[ttt_str] = moves[randint(0, len(moves)-1)]
    return individual
        
def Select(population):
    r = random()
    for i in range(len(PROB)):
        if r <= PROB[i]:
            return copy.deepcopy(population[i])

#d1, d2: two individuals
def Crossover(d1, d2):
    d = {}
    for key in d1.keys():
        r = random()
        if r <= prob_crossover:
            d[key] = d1[key]
        else:
            d[key] = d2[key]
    return d
            
#d: individual
#d[i][0]: encode of state i
#d[i][1]: move of state i        
def Mutate(d):
    for key in d.keys():
        if random() <= prob_mutation:
            moves = INDIVIDUAL_TEMPLATE[key]
            d[key] = moves[randint(0, len(moves)-1)]
            
def CalculateFitness():
    PLAY_NUM = [0]*population_num
    LOST_NUM = [0]*population_num
    for i in range(population_num):
        ttt = TicTacToe()
        lost_num, play_num = PlayGameAsFirst(ttt, POPULATION[i])
        LOST_NUM[i] += lost_num
        PLAY_NUM[i] += play_num
        ttt = TicTacToe()
        lost_num, play_num = PlayGameAsSecond(ttt, POPULATION[i])
        LOST_NUM[i] += lost_num
        PLAY_NUM[i] += play_num
    fitness_sum = 0
    for i in range(population_num):
        FITNESS[i] = 1 - LOST_NUM[i]/PLAY_NUM[i]
        fitness_sum += FITNESS[i]
    return fitness_sum

def PlayGameAsFirst(ttt, d):
    all_lost_num = 0
    all_play_num = 0
    result = ttt.isGameOver()
    if result != None:
        if result == TicTacToe.WHITEWIN:
            return 1, 1
        else:
            return 0, 1
    ttt_str = ttt.ToString()
    base_str = STATE[ttt_str]
    move = GenEquivalentMove(base_str, d[base_str], ttt_str)
    ttt.play(*move)
    result = ttt.isGameOver()
    if result != None:
        if result == TicTacToe.WHITEWIN:
            return 1, 1
        else:
            return 0, 1
        
    moves = ttt.getAllMoves()
    for move in moves:
        node = ttt.clone()
        node.play(*move)
        result = node.isGameOver()
        if result != None:
            if result == TicTacToe.WHITEWIN:
                all_lost_num += 1
            all_play_num += 1
        else:
            lost_num, play_num = PlayGameAsFirst(node, d)
            all_lost_num += lost_num
            all_play_num += play_num

    return all_lost_num, all_play_num

def PlayGameAsSecond(ttt, d):
    all_lost_num = 0
    all_play_num = 0
    result = ttt.isGameOver()
    if result != None:
        if result == TicTacToe.BLACKWIN:
            return 1, 1
        else:
            return 0, 1
        
    moves = ttt.getAllMoves()
    for move in moves:
        node = ttt.clone()
        node.play(*move)
        result = node.isGameOver()
        if result != None:
            if result == TicTacToe.BLACKWIN:
                all_lost_num += 1
            all_play_num += 1
        else:
            ttt_str = node.ToString()
            base_str = STATE[ttt_str]
            move = GenEquivalentMove(base_str, d[base_str], ttt_str)
            node.play(*move)
            result = node.isGameOver()
            if result != None:
                if result == TicTacToe.BLACKWIN:
                    all_lost_num += 1
                all_play_num += 1
            else:
                lost_num, play_num = PlayGameAsSecond(node, d)
                all_lost_num += lost_num
                all_play_num += play_num

    return all_lost_num, all_play_num

def GetBestIndividual():
    max_fitness = -sys.maxsize
    max_individual = None
    for i in range(population_num):
        if max_fitness < FITNESS[i]:
            max_fitness = FITNESS[i]
            max_individual = copy.deepcopy(POPULATION[i])
    return max_individual

def main():
    global INDIVIDUAL_TEMPLATE, STATE, MAX_FITNESS, AVERAGE_FITNESS, MAX_INDIVIDUAL
    try:
        best_file = open('BestIndividual.dat', 'rb')
        best_individual = pickle.load(best_file)
        best_file.close()

        template_file = open('IndividualTemplate.dat', 'rb')
        INDIVIDUAL_TEMPLATE = pickle.load(template_file)
        template_file.close()
        
        state_file = open('State.dat', 'rb')
        STATE = pickle.load(state_file)
        state_file.close()
        
        maxfitness_file = open('MaxFitness.dat', 'rb')
        MAX_FITNESS = pickle.load(maxfitness_file)
        maxfitness_file.close()

        avgfitness_file = open('AverageFitness.dat', 'rb')
        AVERAGE_FITNESS = pickle.load(avgfitness_file)
        avgfitness_file.close()

        maxindividual_file = open('MaxIndividual.dat', 'rb')
        MAX_INDIVIDUAL = pickle.load(maxindividual_file)
        maxindividual_file.close()
        
    except FileNotFoundError:
        Init()
        for t in range(generation_num):
            P_TMP = copy.deepcopy(POPULATION)
            for i in range(population_num):
                seed()
                if random() <= prob_replicate:
                    POPULATION[i] = Select(P_TMP)
                else:
                    d1 = Select(P_TMP)
                    d2 = Select(P_TMP)
                    d = Crossover(d1, d2)
                    Mutate(d)
                    POPULATION[i] = d
                
            fitness_sum = CalculateFitness()
                
            #Update the statistics of population
            PROB[0] = FITNESS[0]/fitness_sum
            for i in range(1, len(FITNESS)):
                PROB[i] = PROB[i-1]+FITNESS[i]/fitness_sum
            
            MAX_FITNESS[t] = max(FITNESS)
            AVERAGE_FITNESS[t] = fitness_sum/population_num
            MAX_INDIVIDUAL[t] = GetBestIndividual()
            print('t = ', t, ' Average Fitness = ', AVERAGE_FITNESS[t], \
                  ' Max Fitness = ', MAX_FITNESS[t])
            if MAX_FITNESS[t] == 1.0:
                break
                
        best_individual = GetBestIndividual()
        
        best_file = open('BestIndividual.dat', 'wb')
        pickle.dump(best_individual, best_file)
        best_file.close()
        
        maxfitness_file = open('MaxFitness.dat', 'wb')
        pickle.dump(MAX_FITNESS, maxfitness_file)
        maxfitness_file.close()

        avgfitness_file = open('AverageFitness.dat', 'wb')
        pickle.dump(AVERAGE_FITNESS, avgfitness_file)
        avgfitness_file.close()

        maxindividual_file = open('MaxIndividual.dat', 'wb')
        pickle.dump(MAX_INDIVIDUAL, maxindividual_file)
        maxindividual_file.close()
        
        plt.plot(T, BEST_FITNESS)
        plt.plot(T, MAX_FITNESS)
        plt.plot(T, AVERAGE_FITNESS)
        plt.show()
        
    win = GraphWin('GA for TicTacToe', 600, 600, autoflush=False)
    ttt = TicTacToe()
    tttdraw = TTTDraw(win)
    tttinput = TTTInput(win)
    tttdraw.draw(ttt)
    
    while win.checkKey() != 'Escape':
        if ttt.getPlayer() == TicTacToe.WHITE:
            ttt_str = ttt.ToString()
            base_str = STATE[ttt_str]
            move = GenEquivalentMove(base_str, best_individual[base_str], ttt_str)
            if move != ():
                ttt.play(*move)
        tttinput.input(ttt)
        tttdraw.draw(ttt)
        if ttt.isGameOver() != None:
            time.sleep(1)
            ttt.reset()
            tttdraw.draw(ttt)
            #win.getMouse()
    win.close()
    
if __name__ == '__main__':
    main()