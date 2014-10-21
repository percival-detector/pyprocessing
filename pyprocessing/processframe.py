# processframe.py
#
# Author: Arvinder Palaha
import numpy as np

def ADUcorrection(ADUc,Oc,Gc,Oct,Gct,ADUf,Of,Gf,Oft,Gft):
    ADUcor  = ((ADUc-Oc)/Gc) * Gct + Oct
    ADUcor -= ((ADUf-Of)/Gf) * Gft + Oft
    return ADUcor

def a2d_gain(number):
    return int('{:02b}'.format( number & 3 )[::-1], 2)

def a2d_fine(number):
    return int('{:08b}'.format( (number & 2**8-1<<2) >> 2)[::-1], 2)

def a2d_coarse(number):
    return int('{:05b}'.format( number>>10 & 2**5-1)[::-1], 2)

def d2a_gain(ADUgain):
    return int('{:02b}'.format(ADUgain & 3)[::-1],2)

def d2a_coarse(ADUc):
    return int('{:16b}'.format( (ADUc & 2**5-1) )[::-1],2)<<10

def d2a_fine(ADUf):
    return int('{:16b}'.format( (ADUf & 2**8-1) )[::-1],2)<<2

def ADUcoarsefinegain(number,Gct=2**8,Oct=2**8-1):
    coarse = int(number+Oct)/int(Gct)
    fine = (Gct - 1) - ((number-1) % Gct)
    gain = (number>>13)&3
    return coarse,fine,gain

def digital2analogpixel(digitalpixel):
    coarse,fine,gain = ADUcoarsefinegain(digitalpixel)
    return d2a_gain(gain) + d2a_fine(fine) + d2a_coarse(coarse)

class processor:

    def __init__(self,
        Oct=2**8-1,Gct=2**8,Oft=0,Gft=1,
        Oc=0, Gc=1, Of=0, Gf=1
        ):
        self.coarseOffset = Oc
        self.coarseGain = Gc
        self.fineOffset = Of
        self.fineGain = Gf
        self.coarseOffsetTarget = Oct
        self.coarseGainTarget = Gct
        self.fineOffsetTarget = Oft
        self.fineGainTarget = Gft