#-*- coding: utf-8 -*-
import threading
from time import sleep
from PyQt4.QtCore import QObject, SIGNAL
from serial import Serial as PySerial
import serial
import serial.tools.list_ports as stlp
import config

class Serial(threading.Thread):

    PARITIES = [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD]
    BYTESIZES = [8, 7, 6, 5]
    STOPBITSES = [1, 1.5, 2]

    SIG_NEWDATA = "SIG_NEWDATA"
    SIG_RECVEXCEPTION = "SIG_RECVEXCEPTION"

    def __init__(self):
        threading.Thread.__init__(self)
        self.qtobj = QObject()
        self.__terminate = False

    @classmethod
    def getActivePorts(self):
        """获取当前活动的串口列表"""

        return [ devInfo[0] for devInfo in list(stlp.comports()) ]

    def open(self, settings):
        try:
            self.serial = PySerial(settings["port"], settings["baund"], settings["bytesize"],
                                       settings["parity"], settings["stopbits"], settings["timeout"])
            self.serial.flushInput()
            self.serial.flushOutput()

        except Exception, msg:
            return False, msg.__str__()

        return True, "success"

    def resetDevice(self):
        self.serial.setDTR(0)
        sleep(0.1)
        self.serial.setDTR(1)

    def terminate(self):
        self.__terminate = True

    def send(self, data, _type):
        try:
            self.serial.write(data)
            return True
        except Exception:
            print e
            return False

    def recv(self):
        data = ""
        while 1:
            if self.__terminate:
                break

            data = self.serial.read(1)
            if data == '':
                continue
            sleep(config.mergeInterval * 0.001)   # 合并mergeInterval毫秒内达到的数据, 当前的这个写法是有问题的，待修复
            n = self.serial.inWaiting()
            data = "%s%s" % (data, self.serial.read(n))
            break;

        return data

    def close(self):
        if self.serial.isOpen():
            self.serial.close()

    def run(self):
        data = None
        while 1:
            try:
                data = self.recv()
            except Exception:
                self.qtobj.emit(SIGNAL(Serial.SIG_RECVEXCEPTION))
                break

            if not data:
                break

            self.qtobj.emit(SIGNAL(Serial.SIG_NEWDATA), data)

        self.serial.close()
