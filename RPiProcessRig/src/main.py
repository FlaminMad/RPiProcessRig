#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   25/10/2016
@rev:    1
@lang:   Python 2.7
@deps:   <None>
@desc:   Main file to start the MODBUS server and IO sampling system
"""

import time
from threading import Thread
from modbusServer import modbusServer
from IOSampler import IOSampler

# Initialise Instances
mServ = modbusServer()
IO = IOSampler()

def modbusFunc(mServ): 
    print("Server starting")
    mServ.runServer()
    
def IOFunc(mServ, IO):
    while(True):
        print("IO sampler starting")
        if IO.runSampler(mServ) == 2:
            break
        time.sleep(1)
        print("Respawning IO Sampler")


MF = Thread(target=modbusFunc, args = (mServ,))
IO = Thread(target=IOFunc, args = (mServ,IO))
MF.start()
IO.start()
IO.join()
mServ.stopServer()
print "Exiting!"
