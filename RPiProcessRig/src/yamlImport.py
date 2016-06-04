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

import yaml

class yamlImport():
    
    @staticmethod
    def importYAML(pathToFile):
        try:
            with open(pathToFile, "r") as f:
                config = yaml.load(f)
        except IOError:
            print("Failed to read " + pathToFile)
            raise SystemExit()
        return config