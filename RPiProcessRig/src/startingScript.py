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
from threading import Thread
from modbusServer import modbusServer
from IOSampler import IOSampler

# Initialise Instances
mServ = modbusServer()
IO = IOSampler()

def modbusFunc(mServ): 
    while(True):
        print("Server starting")
        mServ.runServer()
        time.sleep(1)
        print("Respawning MODBUS Server")
    
def IOFunc(mServ, IO):
    while(True):
        print("IO sampler starting")
        if IO.runSampler(mServ) == 2:
            break
        time.sleep(1)
        print("Respawning TO Sampler")


MF = Thread(target=modbusFunc, args = (mServ,))
IO = Thread(target=IOFunc, args = (mServ,IO))
MF.start()
IO.start()
IO.join()
mServ.servTCP.server_close()
mServ.servTCP.shutdown()
print "Exiting!"