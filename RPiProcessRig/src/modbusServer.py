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
import socket
from .yamlImport import yamlImport

from pymodbus.server.sync import ModbusTcpServer
from pymodbus.server.sync import ModbusSerialServer
from pymodbus.transaction import ModbusRtuFramer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder


class modbusServer():

    def __init__(self):
        self.__logging()
        self.cfg = yamlImport.importYAML("./cfg/modbusSettings.yaml")
        self.builder = BinaryPayloadBuilder(endian=Endian.Little)
        self.__setupContext()
        self.__serverInfo()
        self.__configureServer()

    def __logging(self):
        import logging
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.INFO)
    
    def __setupContext(self):
        #Setup Coils
        co = ModbusSequentialDataBlock(1, [0]*1)
        di = ModbusSequentialDataBlock(1, [0]*6)
        
        #Setup Registers (Inc floats)
        for i in range(0,3):
            self.builder.add_32bit_float(0.0)
        ir = ModbusSequentialDataBlock(1, self.builder.to_registers())
        
        for i in range(0,3):
            self.builder.add_32bit_float(0.0)
        hr = ModbusSequentialDataBlock(1, self.builder.to_registers())
        
        #Setup datastore
        store = ModbusSlaveContext(co=co,di=di,hr=hr,ir=ir)
        self.context = ModbusServerContext(slaves=store, single=True)


    def __serverInfo(self):
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName  = self.cfg["VendorName"]
        self.identity.VendorUrl   = self.cfg["VendorUrl"]
        self.identity.ProductName = self.cfg["ProductName"]
        self.identity.ModelName   = self.cfg["ModelName"]
        self.identity.MajorMinorRevision = self.cfg["Revision"]
    
    def __getIPAddress(self):
        if self.cfg["manualIP"] == "N":
            return socket.gethostbyname(socket.gethostname())
        return self.cfg["ip"]
    
    def __configureServer(self):
        if self.cfg["method"] == "tcp":
            self.servTCP = ModbusTcpServer(self.context, 
                                           identity=self.identity, 
                                           address=(self.__getIPAddress(),
                                                    self.cfg["tcpPort"]))
        elif self.cfg["method"] == "rtu":
            self.servRTU = ModbusSerialServer(self.context,
                                             framer=ModbusRtuFramer,
                                             identity=self.identity,
                                             port=self.cfg["rtuPort"],
                                             stopbits=self.cfg["stopbits"],
                                             bytesize=self.cfg["bytesize"],
                                             parity=self.cfg["parity"],
                                             baudrate=self.cfg["baudrate"],
                                             timeout=self.cfg["timeout"])
        else:
            raise ReferenceError("Invalid server type")
            
    def runServer(self):
        if self.cfg["method"] == "tcp":
            self.servTCP.serve_forever()
        elif self.cfg["method"] == "rtu":
            self.servRTU.serve_forever()
        else:
            raise ReferenceError("Invalid server type")
    
    def stopServer(self):
        if self.cfg["method"] == "tcp":
            self.servTCP.server_close()
            self.servTCP.shutdown()
        elif self.cfg["method"] == "rtu":
            self.servRTU.server_close()
        else:
            raise ReferenceError("Invalid server type")
        
    def encodeData(self,data):
        self.builder.reset()
        try:
            for i in range(0,len(data)):
                self.builder.add_32bit_float(data[i])
        except TypeError:
            self.builder.add_32bit_float(data)
        return self.builder.to_registers()
    
    def decodeData(self,data):
        returnData = [0]*(len(data)/2)
        decoder = BinaryPayloadDecoder.fromRegisters(data, endian=Endian.Little)
        for i in range(0,len(data)/2):
            returnData[i] = round(decoder.decode_32bit_float(),2)
        return returnData