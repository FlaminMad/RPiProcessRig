#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   03/06/2016
@rev:    1
@lang:   Python 2.7
@deps:   RPi.GPIO, spidev
@desc:   Interface for the RPI GPIO pins. Note that the spidev kernel module
         spi-bcm2735 or similar needs to be loaded.
"""
import time
import spidev
import RPi.GPIO as gpio
from osTools import osTools
from yamlImport import yamlImport

class gpioInterface():
    
    def __init__(self):
        #Create Instances
        osTool = osTools()      
        self.spi = spidev.SpiDev()

        #Load Settings
        self.cfg = yamlImport.importYAML("../cfg/IOConfig.yaml")
        
        #Initial Setup        
        if osTool.checkAdmin() == False:
            raise IOError("Admin Rights Required To Access GPIO Header")
        self.__configureIO()
	
    def pumpPWMstart(self, dc):
        self.pwm = gpio.PWM(self.cfg["pump"],self.cfg["pwmHz"])
        if dc <> 100:
            self.pwm.start(100)
            time.sleep(0.1)
            self.pumpPWMalter(0,dc)
        else:
            self.pwm.start(100)
	
    def pumpPWMalter(self, Hz, dc):
        if Hz != 0:
            self.pwm.ChangeFrequency(Hz)
        if dc != 0:
		self.pwm.ChangeDutyCycle(dc)
	
    def pumpPWMstop(self):
        self.pwm.stop()
        
    def readADC(self):
        adc = self.spi.xfer2([1,(8+self.cfg["LTChannel"])<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def alarmsT2(self):
        #TODO: Harware not yet installed
        #TODO: Needs to consist of two inputs, one high level and one low in T2
        NotImplementedError
        return 0

    def cleanUp(self):
        gpio.cleanup()
        self.spi.close()

    def __configureIO(self):
        try:
            gpio.setmode(gpio.BCM)
            gpio.setup(self.cfg["pump"], gpio.OUT)
            self.spi.open(self.cfg["spiBus"],self.cfg["spiDevice"])
        except:
            raise SystemExit(IOError)