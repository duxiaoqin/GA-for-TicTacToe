# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 07:39:28 2018

@author: duxiaoqin
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

T = range(1517)
BEST_FITNESS = [1]*1517

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
plt.plot(T, MAX_FITNESS[:1517])
plt.plot(T, AVERAGE_FITNESS[:1517])
plt.show()