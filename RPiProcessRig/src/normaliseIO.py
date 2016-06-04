#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sat Jun 04/06/2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   Functions to convert the hardware data to sensible numbers/scales
"""

from yamlImport import yamlImport

class normaliseIO():
    
    def __init__(self):
        self.cfg = yamlImport.importYAML("../cfg/IOConfig.yaml")
        self.__pwmEqn()

    
    def adcConv(self,adcVal):
        return ((self.cfg["adcM"]*adcVal) + self.cfg["adcC"])

    
    def pwmConv(self,softPWM):
        hardPWM = round(((self.pwmM * softPWM) + self.pwmC),1)
        if hardPWM <= self.cfg["pwmMin"]:
            return 0
        elif hardPWM >= self.cfg["pwmMax"]:
            return self.cfg["pwmMax"]
        else:
            return hardPWM
    
    def __pwmEqn(self):
        # M and C represent a line of the form Y = Mx + C
        self.pwmM = (self.cfg["pwmMax"] - self.cfg["pwmMin"]) / self.cfg["pwmMax"]
        self.pwmC = self.cfg["pwmMin"]