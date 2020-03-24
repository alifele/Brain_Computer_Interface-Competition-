# -*- coding: utf-8 -*-
"""plotters.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X8o7essoDXMP16f084ciIn7XhvZjtdSG
"""

import numpy as np
import matplotlib.pyplot as plt

def pos_finder(chan):
  scalp = [(1,4),(0,3),(0,5),(1,2),(1,6)] + [(2,i) for i in range(0,9,2)]
  scalp += [(3,i) for i in range(1,8,2)]
  scalp += [(4,i) for i in range(0,9,2)]
  scalp += [(5,i) for i in range(1,8,2)]
  scalp += [(6,i) for i in range(0,9,2)]
  scalp += [(7,2), (7,6), (8,2), (8,6)]
  scalp += [(1,0), (1,8)]

  scalp += [(2,i) for i in range(1,8,2)]
  scalp += [(3,i) for i in range(0,9,2)]

  scalp += [(4,i) for i in range(1,8,2)]
  scalp += [(5,i) for i in range(0,9,2)]

  scalp += [(6,i) for i in range(1,8,2)]
  scalp += [(7,0), (7,4), (7,8)]
  scalp += [(8,4), (8,1), (8,8), (8,0)]
  
  return scalp[chan]

def scalp_plotter(channels_data,t):
  '''
  provide the channels data, this function will plot the scalp map
  '''
  channel = 0
  mat = np.zeros((9,9))
  for i in range(8):
    for j in range(8):
      if(channel==63):
        break
      pos = pos_finder(channel)
      mat[pos[0], pos[1]]=channels_data[t,channel]
      channel +=1

  return mat

