#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sat Jun 04 17:40:27 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   <>
"""

from normaliseIO import normaliseIO
from gpioInterface import gpioInterface
import time

def main():
    IO = gpioInterface()
    conv = normaliseIO()
    x = 0
    IO.pumpOn()
    while x < 100:
        x = conv.adcConv(IO.readADC(7))
        time.sleep(2)
    IO.pumpOff()
    IO.cleanUp()