#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   03/06/2016
@rev:    1
@lang:   Python 2.7
@deps:   RPi.GPIO, spidev, osTools
@desc:   Interface for the RPI GPIO pins. Note that the spidev kernel module
         spi-bcm2735 or similar needs to be loaded.
"""

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
    
    def pumpOn(self):
        gpio.output(self.cfg["PUMP"],gpio.HIGH)
    
    def pumpOff(self):
        gpio.output(self.cfg["PUMP"],gpio.LOW)
	
    def pumpPWMstart(self, Hz, dc):
        self.pwm = gpio.PWM(self.cfg["PUMP"],Hz)
        self.pwm.start(dc)
	
    def pumpPWMalter(self, Hz, dc):
        if Hz != 0:
            self.pwm.ChangeFrequency(Hz)
        if dc != 0:
		self.pwm.ChangeDutyCycle(dc)
	
    def pumpPWMstop(self):
        self.pwm.stop()
	
    def readADC(self, channel):
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
	
    def cleanUp(self):
        gpio.cleanup()
        self.spi.close()

    def __configureIO(self):
        try:
            gpio.setmode(gpio.BCM)
            gpio.setup(self.cfg["PUMP"], gpio.OUT)
            self.spi.open(self.cfg["spiBus"],self.cfg["spiDevice"])
        except:
            raise SystemExit(IOError)