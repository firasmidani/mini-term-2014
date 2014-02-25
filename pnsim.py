"""
pnsim.py -- a module for exploring network dynamics using the boolean approximation.
    Created to illustrate simple network motifs as described in 
    Alon 2007, An Introduction to Systems Biology: Design Principles of Biological Circuits
"""

import math
import operator
import inspect
from functools import partial



class Node(list):
    def __init__(self, logicfxn, initval=0):
        list.__init__(self)
        self.initval = initval
        self.now = initval
        self.logicfxn = logicfxn

    def reset(self, newinit=None):
        if newinit is not None:
            self[:] = []
            self.now = newinit
        else:
            self[:] = []
            self.now = self.initval
            
    def update(self, *inputs):
        beta, alpha = self.logicfxn(*inputs)
        delta = beta - alpha * self.now
        self.now = self.now + delta
        self.append(self.now)

    def evaluate(self, *inputs):
        [self.update(*x) for x in zip(*inputs)]





#-------------------------------------------------------------------------

def get_reqargs(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)]
    return args 
    
def get_kwdefaults(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if defaults:
        args = args[-len(defaults):]
        return dict(zip(args,defaults))
    return None

    
        
#-------------------------------------------------------------------------
# Examples        

import numpy as np
from matplotlib import pylab


def pulse(ontime, offtime,  ntimes=100, onval=1):
    if ontime >= offtime:
        raise Exception("Invalid on/off times.")
    signal = np.zeros(ntimes)
    signal[ontime:offtime] = onval
    return signal
    
def noisy_pulse(ontime, offtime, ntimes=100, onval=1, sd=0.2):
    signal = pulse(ontime,offtime,ntimes=ntimes, onval=onval)
    noise = np.random.normal(0,sd,len(signal))
    return signal + noise


def example_simplereg():
    ylogic = lambda x: (0.2,0.1) if (x > 0.5) else (0,0.1)
    
    x = pulse(10,800)
    y = Node(ylogic)

    y.evaluate(x)
    return x,y

def example_negauto():
    def ylogic(x,y): 
        if (x > 0.5 and y < 0.5):
            return (0.4, 0.1)
        elif (x > 0.5 and y >= 0.5):
            return (0.2, 0.1)
        else:
            return (0, 0.1)
    
    x = pulse(10,800)
    y = Node(ylogic)

    for i in range(len(x)):
        y.update(x[i], y.now)

    return x,y

def example_posauto():
    def ylogic(x,y): 
        if (x > 0.5 and y < 0.5):
            return (0.2, 0.1)
        elif (x > 0.5 and y >= 0.5):
            return (0.5, 0.1)
        else:
            return (0, 0.1)
    
    x = pulse(10,800)
    y = Node(ylogic)

    for i in range(len(x)):
        y.update(x[i], y.now)

    return x,y


    
def example_coherent():
    ylogic = lambda x: (0,0.1) if (x < 0.5) else (0.2,0.1)
    zlogic = lambda x,y: (0.2,0.1) if (x > 0.5 and y > 1) else (0,0.1)
    
    x = pulse(10,80)
    y = Node(ylogic)
    z = Node(zlogic)
    
    y.evaluate(x)
    z.evaluate(x,y)
    
    times = range(len(x))
    pylab.plot(times, x, times, y, times, z)
    return x,y,z

    

    

def example_incoherent():
    ylogic = lambda x: (0,0.1) if (x < 0.5) else (0.2,0.1)
    zlogic = lambda x,y: (0,0.1) if (x < 0.5) else  \
                         ((0.2,0.1) if (x >= 0.5 and y < 1) else (0.025,0.1))
    
    x = pulse(10,80)
    y = Node(ylogic)
    z = Node(zlogic)
    
    y.evaluate(x)
    z.evaluate(x,y)
    
    times = range(len(x))
    pylab.plot(times, x, times, y, times, z)
    return x,y,z
    
    
def example_repressilator(n=500):
    def ylogic(x): return (0.8, 0.1) if (x < 0.5) else (0, 0.1)
    def zlogic(y): return (0.8, 0.1) if (y < 0.5) else (0, 0.1)
    def xlogic(z): return (0.8, 0.1) if (z < 0.5) else (0, 0.1)
    
    y0 = 2
    z0 = 2
    x0 = 2
    
    x,y,z = [x0], [y0], [z0]
    
    y = Node(ylogic, y0)
    z = Node(zlogic, z0)
    x = Node(xlogic, x0)
    
    for i in range(n):
        #xnow, ynow, znow = x.now,y.now,z.now
        x.update(z.now)
        y.update(x.now)
        z.update(y.now)
        
    return x, y, z
        

class Node_rayleigh(Node):
    def update(self, x):
        beta, alpha = self.logicfxn(x)
        beta = np.random.rayleigh(beta)
        alpha = np.random.rayleigh(alpha)
        delta = beta - alpha * self.now
        self.now = self.now + delta
        self.append(self.now)      
                
def example_noisyrepressilator(n=500):
    rd = np.random.rayleigh
    def ylogic(x): return (0.8, 0.1) if (x < rd(0.5)) else (0.01, 0.1)
    def zlogic(y): return (0.8, 0.1) if (y < rd(0.5)) else (0.01, 0.1)
    def xlogic(z): return (0.8, 0.1) if (z < rd(0.5)) else (0.01, 0.1)
    
    y0 = 2
    z0 = 2
    x0 = 2
    
    x,y,z = [x0], [y0], [z0]
    
    y = Node_rayleigh(ylogic, y0)
    z = Node_rayleigh(zlogic, z0)
    x = Node_rayleigh(xlogic, x0)
    
    for i in range(n):
        x.update(z.now)
        y.update(x.now)
        z.update(y.now)
        
    return x, y, z
                
    