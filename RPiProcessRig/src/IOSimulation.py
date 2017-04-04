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
from yamlImport import yamlImport


class IOSimulation():
    def __init__(self):
        # Initialise Instances
        self.alarmCfg = yamlImport.importYAML("../cfg/alarms.yaml")
        self.cfg = yamlImport.importYAML("../cfg/IOConfig.yaml")
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
            time.sleep(self.cfg["interval"] - (time.time() - loopTime))

    
    def __pumpCtrl(self,mServ):
        #Decode registers
        floatReg = mServ.decodeData(mServ.context[0].getValues(3,0,10))
        
        #Alter Pump Duty Cycle
        if floatReg[0] <> floatReg[1]:
            hardPWM = floatReg[0]
            if mServ.context[0].getValues(2,0,1)[0] == 1:
                if floatReg[0] == 0:
                    mServ.context[0].setValues(2,0,[0]) 														 #Set pump running bit to 0
                    mServ.context[0].setValues(3,2,mServ.encodeData([floatReg[0]])) #Set pump speed to 0
                else:
                    mServ.context[0].setValues(3,2,mServ.encodeData([floatReg[0]])) #Update pump speed
            else:
                if floatReg[0] <> 0:
                    mServ.context[0].setValues(2,0,[1]) 														 #Set pump running bit to 1
                    mServ.context[0].setValues(3,2,mServ.encodeData([floatReg[0]])) #Update pump speed
            mServ.context[0].setValues(3,4,mServ.encodeData([floatReg[0]]))         #N/A in sim mode
        
        #Alter Pump PWM Frequency
        if floatReg[3] <> floatReg[4]:
            mServ.context[0].setValues(3,8,mServ.encodeData([floatReg[3]]))
        
    
    def __adcRead(self, mServ):
        mServ.context[0].setValues(4,4,mServ.encodeData([0.0])) #Calibrated value set to zero as N/A in sim mode
        
        self.adcVal = 1 #Insert equation here relating to pump speed and time
        # At this point we know the time elapsed since last run with cfg.interval
        # Could do with a 2D equation relating both tank level and pump speed to flow
        # Use collected data to obtain
        # Would also be good to add noise to the signal for realism
        
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
        #Not applicable in SIM mode
    
    
    def __heartbeatCounter(self, mServ):
        # Check sample loop is 'still alive'
        self.count += 1
        if self.count == 65535:
            self.count = 0
        else:
            mServ.context[0].setValues(4,2,mServ.encodeData([self.count]))
    
    
    def __loadPWMFreq(self, mServ):
        # Not a usable function in simulation mode
        # Therefore, set an arbitary value of 70
        mServ.context[0].setValues(3,6,mServ.encodeData([70,70]))
        
        
    def __shutdown(self, mServ):
        # Not applicable in simulation mode
        pass