#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from ctypes import cdll

prefix = "./DynamixelSDK"

if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    if sys.maxsize > 2**32:
        # for windows 64bit
        dxl_lib = cdll.LoadLibrary(prefix + "/c/build/win64/output/dxl_x64_c.dll")
    else:
        # for windows 32bit
        dxl_lib = cdll.LoadLibrary(prefix + "/c/build/win32/output/dxl_x86_c.dll")
elif sys.platform.startswith('darwin'):
    # for Mac OS
    dxl_lib = cdll.LoadLibrary(prefix + "/c/build/mac/libdxl_mac_c.dylib")
else:
    if sys.maxsize > 2**32:
        # for linux 64bit
        dxl_lib = cdll.LoadLibrary(prefix + "/c/build/linux64/libdxl_x64_c.so")
    else:
        # for linux 32bit
        dxl_lib = cdll.LoadLibrary(prefix + "/c/build/linux32/libdxl_x86_c.so")


portHandler = dxl_lib.portHandler
openPort = dxl_lib.openPort
closePort = dxl_lib.closePort
setBaudRate = dxl_lib.setBaudRate

packetHandler = dxl_lib.packetHandler
printTxRxResult = dxl_lib.printTxRxResult
getTxRxResult = dxl_lib.getTxRxResult
getLastTxRxResult = dxl_lib.getLastTxRxResult
getLastRxPacketError = dxl_lib.getLastRxPacketError

read1ByteTxRx = dxl_lib.read1ByteTxRx
read2ByteTxRx = dxl_lib.read2ByteTxRx
read4ByteTxRx = dxl_lib.read4ByteTxRx
write1ByteTxRx = dxl_lib.write1ByteTxRx
write2ByteTxRx = dxl_lib.write2ByteTxRx
write4ByteTxRx = dxl_lib.write4ByteTxRx
