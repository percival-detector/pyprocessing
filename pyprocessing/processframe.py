# processframe.py
#
# Author: Arvinder Palaha
import numpy as np

def ADUcorrection(ADUc,Oc,Gc,Oct,Gct,ADUf,Of,Gf,Oft,Gft):
    ADUcor  = ((ADUc-Oc)/Gc) * Gct + Oct
    ADUcor -= ((ADUf-Of)/Gf) * Gft + Oft
    return ADUcor

def extractgain(number):
    return int('{:02b}'.format( number & 3 )[::-1], 2)

def extractfine(number):
    return int('{:08b}'.format( (number & 2**8-1<<2) >> 2)[::-1], 2)

def extractcoarse(number):
    return int('{:05b}'.format( number>>10 & 2**5-1)[::-1], 2)

def ADUcoarsefine():
    pass