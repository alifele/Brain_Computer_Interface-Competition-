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



def transform_1(x,y):
  x = x/ 2
  y = y/2
  y_ = y
  y = x
  x = y_
  return x,y


def transform_2(x,y):
  x = x/2
  y = y/2
  d = (x[2] - x[0]) 
  D = (x[-1] - x[0] )
  y  = y+d+D
  return x,y


def transform_3(x,y):
  x = x/2
  y = y/2
  d = (x[2] - x[0]) 
  D = (x[-1] - x[0] )
  y = y + D +  d
  x = x + D + d
  return x,y


def transform_4(x,y):
  x = x/2
  y = y/2
  d = (x[2] - x[0]) 
  D = (x[-1] - x[0])
  a = x[-1]
  x_ = a-y
  y_ = a-x

  x = x_
  y = y_
  
  x = x+d+D


  return x,y


def Hilbert_generator(n=5):
  '''
  by default this function will generate level 5 Hilbert curve which can condence 2^12 = 4096
  data into a matrix with size xint[-1] + 1. In which the x_int is x_int = x * 1/(x[2]-x[0])
  '''
  x = np.array([0,0,1,1])
  y = np.array([0,1,1,0])
  for i in range(n):
    img_x = []
    img_y = []
    img_x += transform_1(x,y)[0].tolist()
    img_y += transform_1(x,y)[1].tolist()
    img_x += transform_2(x,y)[0].tolist()
    img_y += transform_2(x,y)[1].tolist()
    img_x += transform_3(x,y)[0].tolist()
    img_y += transform_3(x,y)[1].tolist()
    img_x += transform_4(x,y)[0].tolist() 
    img_y += transform_4(x,y)[1].tolist()
    x = np.array(img_x)
    y = np.array(img_y)
  return x,y


def Hilbert_concat(x,y):

  '''
  this will concatenate tow Hilbert curves side by side in order to increase 
  the amount of data that we want to condence into matrix

  this function can increase the amount of data linearly (consider the way that
  you want to increase the amount of the data by increasin the Hilbert level wich will 
  enlarge the amount of data with factor of 4)


  '''
  x_ = x.tolist()
  x__ = x + (x[2]-x[0]) + x[-1]
  x__ = x__.tolist()
  x = x_ + x__
  y = y.tolist() + y.tolist()

  return np.array(x), np.array(y)



def data_to_HilbertMat(x,y,data=None, padding = 0, test=False, double_factor=1):

  '''
  this function will condence the data into a matrix with a Hilbert curve order

  if you want to check the functionality of the function do not pass any data.
  instead set test as True.

  If you are passing any concatinated Hilbert curve, set the double_factor to the 
  number of blocks that you have put aside of each other.
  For example if you have used Hilbert_concat once, then you should set the double_factor
  equal to 2
  '''

  x_int = x * 1/(x[2]-x[0])
  y_int = y * 1/(y[2]-y[0])
  mat = np.zeros((int((x_int[-1]+1)/double_factor), int(x_int[-1]+1)))
 


  if test == True:
    x = np.linspace(0,20,x_int.shape[0])
    data = np.sin(2*np.pi*1*x) + np.random.randn()

  if data.shape[0]<len(x):
    diff = len(x) - len(data)
    data = data.tolist()
    data = data + [padding] * (diff)
    data = np.array(data)


  #for i in range(mat.shape[1]):
   # for j in range(mat.shape[0]):
    #  mat[int(x_int[m]), int(y_int[m])] = data[m]
      #print(x_int[m])
     # m+=1

  m = 0
  while m<data.shape[0]:
    mat[int(y_int[m]), int(x_int[m])] = data[m]
    #print(x_int[m])
    m+=1

  return mat






############ Garmian #####################3

def Scaler(x):
  max_ = x.max()
  min_ = x.min()
  X = (x-max_ + x-min_)/(max_ - min_)
  return X


def Garmian_calculator(data):
  data = Scaler(data)
  Gar = data.reshape((-1,1)) * data.reshape((1,-1)) - ((1-data**2)**2).reshape((-1,1)) * ((1-data**2)**2).reshape((1,-1))
  return Gar



################# Markov Transition Matrix ####################3
def Markov_matrix_generator(bins, data, normal = True):
  data = np.array(data)
  b0 = bin_finder(bins, data[0])
  W = np.zeros((len(bins), len(bins)))
  for item in range(1,len(data)):
    b1 = bin_finder(bins, data[item])
    W[b0,b1]+=1
    b0 = b1

  if normal == True:
    W = W / (W.sum(axis=1, keepdims = True) + 0.000001)  # This will normalize the W in which the transition probability in each row will sum to 1
    return W

  return W




def bin_finder(bins, n):
  '''
  for example:
    suppose that out bins is like this [1,3,5,7,9]

    so this function will return the following values for 1.5, 3.45, 1, 5

    1.5  ----> 0
    3.45 ----> 1
    1    ----> 0
    5    ----> 2
  '''
  eps = 0.0001
  d = bins[2] - bins[1]
  n+=eps
  return np.argmax((n>bins) * ((n-d)<bins))


def bin_creator(data, n):
  max_ = data.max()
  min_ = data.min()
  bins = np.linspace(np.ceil(min_)-1,np.floor(max_),n)
  return bins


def EEG_plotter(channels, data, size=(15,12), font=10):
  fig = plt.figure(figsize=(15,12))
  diff = np.max(data)

  ax = fig.add_subplot(1,1,1)
  a = ax.plot(data[:,:channels] + (diff+3)*np.arange(channels,0,-1))

  spacing = np.zeros((7200,channels)) + (diff+3)*np.arange(channels,0,-1)
  b = ax.plot(spacing,'--', alpha = 0.8, color='gray')

  c = ax.set_yticks((diff+3)*np.arange(channels,0,-1))
  d = ax.set_yticklabels(['channel{}'.format(i+1) for i in range(channels)], fontsize=font)
  #plt.legend( ['channel{}'.format(i) for i in range(channels) ])






def Localizer(subject_data, save=False):

  #subject_data = subj_1['train_data_class1']
  data = subject_data
  FFT = []
  t = np.linspace(0,3,7200)
  f = np.linspace(1/3, 2400, 7200)
  f_cut_min = 10
  f_cut_max = 150
  for trial in data:
    fft = np.fft.fft(trial.T)
    fft = fft.T
    fft = fft[(f>f_cut_min)*(f<f_cut_max),:]

    FFT.append(fft)
  FFT = np.array(FFT)
  f = f[(f>f_cut_min)*(f<f_cut_max)]
  power = np.sum(np.abs(FFT), axis=1)
  power = np.expand_dims(power, axis=1)
  
  #del_list=np.array([1,2,3,34,33])-1
  #power[:,0:,del_list] = np.mean(power[:,0,:])

  fig = plt.figure(figsize=(10,10))

  for i in range(25):
    ax = fig.add_subplot(5,5,i+1)
    mat = scalp_plotter(power[i], 0)
    im = ax.imshow(mat)
    ax.axis('off')
    #fig.colorbar(im)
  plt.figure()
  a = plt.plot(power[:,0,:].T**0.5)
  #plt.legend(['trial{}'.format(i+1) for i in range(25)])




