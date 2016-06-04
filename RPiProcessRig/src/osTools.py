#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   <none>
Desc:   OS based tools for smooth trasitions between linux & windows
"""

import os
import sys
import ctypes

if os.name == 'nt':
    import msvcrt
else:
    import select


class osTools:

    def __init__(self):
        self.osType = self.__osDetect()
        pass


    def __osDetect(self):
        if os.name == 'nt':
            return 0
        elif os.name == 'posix':
            return 1
        else:
            raise SystemExit("Unsupported OS Type")


    def kbdExit(self):
        if self.osType == 1:
            return self.__linuxExit()
        else:
            return self.__ntExit()


    def checkAdmin(self):
        try:
            admin = os.getuid() == 0
        except AttributeError:
            admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return admin
    
    
    def __linuxExit(self):
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for x in i:
            if x == sys.stdin:
                if sys.stdin.readline()  == 'c\n':
                    return True
        return False


    def __ntExit(self):
        x = msvcrt.kbhit()
        if x:
            if msvcrt.getch() == 'c':
                return True
        return False