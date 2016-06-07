#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sat Jun 04 22:40:49 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   <>
"""

import time
from gpioInterface import gpioInterface
from normaliseIO import normaliseIO


class IOSampler():
    def __init__(self):
        # Initialise Instances
        self.IO = gpioInterface()
        self.conv = normaliseIO()
        self.Interval = 1
    
    def runSampler(self, mServ):
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
        #Alter Pump Duty Cycle
        if mServ.context[0].getValues(3,0,1)[0] <> mServ.context[0].getValues(3,1,1)[0]:
            hardPWM = self.conv.pwmConv(mServ.context[0].getValues(3,0,1)[0])
            if mServ.context[0].getValues(2,0,1)[0] == 1:
                if hardPWM == 0:
                    self.IO.pumpPWMstop()
                    mServ.context[0].setValues(2,0,[0])
                else:
                    self.IO.pumpPWMalter(0,hardPWM)
            else:
                if hardPWM <> 0:
                    self.IO.pumpPWMstart(hardPWM)
                    mServ.context[0].setValues(2,0,[1])
            mServ.context[0].setValues(3,2,[hardPWM])
        
        #Alter Pump PWM Frequency
        if mServ.context[0].getValues(3,3,1)[0] <> mServ.context[0].getValues(3,4,1)[0]:
            if mServ.context[0].getValues(2,0,1)[0] == 1:
                self.IO.pumpPWMalter(mServ.context[0].getValues(3,3,1)[0],0)
                mServ.context[0].setValues(3,4,[mServ.context[0].getValues(3,3,1)[0]])
            else:
                #TODO: Implement a way of changing the default startup frequency
                print("DEBUG: Pump needs to be running")
        
    
    def __adcRead(self, mServ):
         mServ.context[0].setValues(4,0,[self.conv.adcConv(self.IO.readADC())])
        
    
    def __alarmHandling(self, mServ):
        # Alarms for T1 (Tank under control)
        if mServ.context[0].getValues(4,0,1)[0] <= 5:
            mServ.context[0].setValues(2,1,[1,0,0])
        elif mServ.context[0].getValues(4,0,1)[0] >= 95:
            mServ.context[0].setValues(2,1,[0,1,0])
        elif mServ.context[0].getValues(4,0,1)[0] >= 100:
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
        # Ensure the GPIO loop has not frozen
        #TODO: set maximum with reset to zero
        mServ.context[0].setValues(4,1,[(mServ.context[0].getValues(4,1,1)[0]+1)])
    
    
    def __shutdown(self, mServ):
        # Cleanup and shutdown the GPIO safely
        if mServ.context[0].getValues(2,0,1)[0] == 1:
            self.IO.pumpPWMstop()
        self.IO.cleanUp()