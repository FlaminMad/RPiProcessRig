#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   03/06/2016
@rev:    1
@lang:   Python 2.7
@deps:   YAML
@desc:   Class to use as an interface to import YAML files
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
