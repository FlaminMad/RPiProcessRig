#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sat Jun 04 22:40:49 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   Main loop to sample the IO and update the server datastore
"""

import time
from .yamlImport import yamlImport
from .gpioInterface import gpioInterface
from .normaliseIO import normaliseIO


class IOSampler():
    def __init__(self):
        # Initialise Instances
        self.IO = gpioInterface()
        self.conv = normaliseIO()
        self.alarmCfg = yamlImport.importYAML("./cfg/alarms.yaml")
        self.Interval = self.IO.cfg["interval"]
        self.count = 0
    
    
    def run(self, mServ):
        self.__loadPWMFreq(mServ)
        while(True):
            loopTime = time.time()
            self.__pumpCtrl(mServ)                
            self.__adcRead(mServ)
            self.__alarmHandling(mServ)
            self.__heartbeatCounter(mServ)
            if mServ.context[0].getValues(1,0,1)[0] == 1:
                self.__shutdown(mServ)
                return 2
            time.sleep(self.Interval - (time.time() - loopTime))

    
    def __pumpCtrl(self,mServ):
        #Decode registers
        floatReg = mServ.decodeData(mServ.context[0].getValues(3,0,10))
        
        #Alter Pump Duty Cycle
        if floatReg[0] <> floatReg[1]:
            hardPWM = self.conv.pwmConv(floatReg[0])
            if mServ.context[0].getValues(2,0,1)[0] == 1:
                if hardPWM == 0:
                    self.IO.pumpPWMstop()
                    mServ.context[0].setValues(2,0,[0])
                    mServ.context[0].setValues(3,2,mServ.encodeData([floatReg[0]]))
                else:
                    self.IO.pumpPWMalter(0,hardPWM)
                    mServ.context[0].setValues(3,2,mServ.encodeData([floatReg[0]]))
            else:
                if hardPWM <> 0:
                    self.IO.pumpPWMstart(hardPWM)
                    mServ.context[0].setValues(2,0,[1])
                    mServ.context[0].setValues(3,2,mServ.encodeData([floatReg[0]]))
            mServ.context[0].setValues(3,4,mServ.encodeData([hardPWM]))
        
        #Alter Pump PWM Frequency
        if floatReg[3] <> floatReg[4]:
            if mServ.context[0].getValues(2,0,1)[0] == 1:
                self.IO.pumpPWMalter(floatReg[3],0)
                mServ.context[0].setValues(3,8,mServ.encodeData([floatReg[3]]))
            else:
                self.IO.pumpFreqChange(floatReg[3])
                mServ.context[0].setValues(3,8,mServ.encodeData([floatReg[3]]))
        
    
    def __adcRead(self, mServ):
        self.CalVal = self.IO.readADC()
        mServ.context[0].setValues(4,4,mServ.encodeData([self.CalVal]))
        self.adcVal = self.conv.adcConv(self.IO.readADC())
        mServ.context[0].setValues(4,0,mServ.encodeData([self.adcVal]))
        
    
    def __alarmHandling(self, mServ):
        # Alarms for T1 (Tank under control)
        if self.adcVal <= self.alarmCfg["T1LAL"]:
            mServ.context[0].setValues(2,1,[1,0,0])
        elif self.adcVal >= self.alarmCfg["T1LAH"]\
             and self.adcVal < self.alarmCfg["T1LAHH"]:
            mServ.context[0].setValues(2,1,[0,1,0])
        elif self.adcVal >= self.alarmCfg["T1LAHH"]:
            mServ.context[0].setValues(2,1,[0,0,1])
        else:
            mServ.context[0].setValues(2,1,[0,0,0])
        
        # Alarms for T2 (Supply tank)
        if self.IO.alarmsT2 == 1:
            mServ.context[0].setValues(2,4,[1,0])
        elif self.IO.alarmsT2 == 2:
            mServ.context[0].setValues(2,4,[0,1])
        else:
            mServ.context[0].setValues(2,4,[0,0])
    
    
    def __heartbeatCounter(self, mServ):
        self.count += 1
        if self.count == 65535:
            self.count = 0
        else:
            mServ.context[0].setValues(4,2,mServ.encodeData([self.count]))
    
    
    def __loadPWMFreq(self, mServ):
        self.IO.pumpFreqChange(-1)
        mServ.context[0].setValues(3,6,mServ.encodeData([self.IO.pwmHz,self.IO.pwmHz]))
        
        
    def __shutdown(self, mServ):
        # Cleanup and shutdown the GPIO safely
        if mServ.context[0].getValues(2,0,1)[0] == 1:
            self.IO.pumpPWMstop()
        self.IO.cleanUp()