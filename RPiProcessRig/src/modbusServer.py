#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sat Jun 04 20:06:02 2016
@rev:    1
@lang:   Python 2.7
@deps:   pymodbus
@desc:   MODBUS server for the RPiProcessRig project
"""
from yamlImport import yamlImport
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

class modbusServer():

    def __init__(self):
        self.logging()
        self.cfg = yamlImport.importYAML("../cfg/modbusSettings.yaml")
        self.setupContext()
        self.serverInfo()
        self.servTCP = ModbusTcpServer(self.context, 
                                       identity=self.identity, 
                                       address=(self.cfg["ip"], self.cfg["tcpPort"]))
        #TODO: Add option of RTU server as well

    def logging(self):
        import logging
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.INFO)
    
    def setupContext(self):
        store = ModbusSlaveContext(
            co = ModbusSequentialDataBlock(1, [0]*1),
            di = ModbusSequentialDataBlock(1, [0]*6),
            hr = ModbusSequentialDataBlock(1, [0]*5),
            ir = ModbusSequentialDataBlock(1, [0]*2))
        self.context = ModbusServerContext(slaves=store, single=True)

    def serverInfo(self):
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName  = self.cfg["VendorName"]
        self.identity.VendorUrl   = self.cfg["VendorUrl"]
        self.identity.ProductName = self.cfg["ProductName"]
        self.identity.ModelName   = self.cfg["ModelName"]
        self.identity.MajorMinorRevision = self.cfg["Revision"]

    def runServer(self):
        self.servTCP.serve_forever()      