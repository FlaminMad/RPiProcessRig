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
from yamlImport import yamlImport


def modbusFunc(mServ):
    print("Server starting")
    mServ.runServer()
    
def IOFunc(mServ, IO):
    while(True):
        print("IO Code Starting")
        if IO.run(mServ) == 2:
            break
        time.sleep(1)
        print("Respawning IO Code")

def IOMode():
    if yamlImport.importYAML("../cfg/IOConfig.yaml")["simMode"]:
        from IOSampler import IOSampler as IOS
    else:
        from IOSimulation import IOSimulation as IOS
    return IOS
        
# Initialise Instances
mServ = modbusServer()
IO = IOMode()

#Prepare Threads
MF = Thread(target=modbusFunc, args = (mServ,))
IO = Thread(target=IOFunc, args = (mServ,IO))

#Start Program Threads
MF.start()
IO.start()
IO.join()

#Cleanup On Exit Condition
mServ.stopServer()
print "Exiting!"