#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:42:23 2017

@author: rohankamath
"""

import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
pick = open('rick.pkl','rb') #pickle file containing data
y = pickle.load(pick)
import numpy as np


yell2 = y[1]
steps = []
pathdiff = []



for i in range(len(yell2)):
    steps.append(i)
    pathdiff.append(2.441*2*i) #working in nanometers as SciPy has trouble working in metres
    
 
    
def sin (x, lambd, phase, A):
    
    return A * np.sin( ((2*np.pi*x) / lambd) + phase)

def lorentzian(x,gamm):
    
    return (4.166-2.5)*(gamm**2)/((x-3400)**2+gamm**2)

def gaussian(x, sig):
    return 1.666*np.exp(-np.power(x -3400, 2.) / (2 * np.power(sig, 2.)))


lamb = []
amp = []
stepss= []
for j in range(3,49):
    steps3 = pathdiff[100*j:100*(j+1)]
    stepss.append(pathdiff[100*j+50])
    spectrum = yell2 [100*j:100*(j+1)]
    popt, pcov = curve_fit(sin, steps3, spectrum, bounds = ([300,0,0],[800,2*np.pi,np.inf]))
    lamb.append(popt[0])
    amp.append(popt[2])

print(np.average(lamb)) #mean wavelength
print(np.std(lamb)/np.sqrt(len(lamb)))   #error wavelength





peak = []  
peakpos = []
x = []

for i in range(1,len(yell2)-1):
    if yell2[i] > yell2[i-1] and yell2[i] > yell2[i+1]:
        peak.append(yell2[i])
        peakpos.append(steps[i])

x = range(len(peak))
peaknew = peak[0:250] + peak[460:495]
peakposnew = peakpos[0:250]+peakpos[460:495]

peakoffs = []
for i in peaknew:
    peakoffs.append(i - 2.5)
yell2new = []
for i in yell2:
    yell2new.append(i-2.5)

popt,pcov = curve_fit(gaussian,peakposnew,peakoffs)
print(popt[0]*2.441*2e-9) #variance of gaussian
print(popt[0]*2.441*2e-9*2.35) #FWHM of gaussian
perr = np.sqrt(np.diag(pcov))
print(perr*2.441*2e-9*2.35) #error in fit
fit = []


for i in steps:
    fit.append(gaussian(i,(popt[0])))

plt.plot(steps,fit)
plt.plot(steps,yell2new)
plt.show()
