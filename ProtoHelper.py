#-*- coding: utf-8 -*-
import imp
import struct
#import proto.control_pb2 as ctrlpb
import lib.pbjson as pbjson
import util
import config

getPort = lambda nData: struct.unpack("B", nData[3:4])[0]
getSize = lambda nData: struct.unpack("B", nData[4:5])[0]
getCrc  = lambda nData: struct.unpack("B", nData[len(nData) - 1])[0]
getData= lambda nData: nData[5: getSize(nData) + 5]

PORT_CONTROLLER = 0
PORT_CONSOLE = 1

def getMyPbObj():
    try:
        pbobj = imp.new_module("pbobj")
        pycode = open(config.PB_SOURCE_FILE, "r").read()
        exec pycode in pbobj.__dict__
        return pbobj
        
    except Exception as e:
        print e

def pbVisualizedData(nData):
    ctrlpb = getMyPbObj()
    if not ctrlpb:
        return "ERROR TO GET PB OBJECT from %s" % config.PB_SOURCE_FILE
        
    packet = ctrlpb.ControlMessage()
    try:
        packet.ParseFromString(getData(nData))
    except IndexError:
        return "DATA SIZE ERROR"
    except Exception as e:
        return "PARSE PROTO EXCEPTION HAPPENED!"
        
    return pbjson.pb2json(packet)
    
def consoleVisualizedData(nData):
    try:
        return getData(nData)
    except IndexError as e:
        return "INDEX_ERROR"
    
__PORT_CALLBACK_DICT = {
    PORT_CONTROLLER : pbVisualizedData,
    PORT_CONSOLE : consoleVisualizedData
}


def checkProtoData(nData):
    """检查协议数据格式是否正确
    正确返回(True, "OK")
    错误返回(False, ERR-STRING)
    """
    
    if not nData.startswith("\xAA\xBB\xCC"):
        return False, "NOT STARTS WITH 0xAABBCC"
    
    datalen = len(nData)
    if datalen < 6:
        return False, "SIZE TOO SMALL"
        
    size = getSize(nData)
    
    if datalen != size + 6:
        return False, "DATA LEN NOT ENOUGH"
    
    chsum = 0
    for ch in nData[3 : datalen - 1]:
        chsum = (chsum + struct.unpack("B", ch)[0]) % 0xFF
        
    crc = getCrc(nData)
    if crc != chsum:
        return False, "CRC NOT RIGHT"
    
    return True, "OK"

def getVisualizedData(nData):
    ret, errmsg = checkProtoData(nData)
    if not ret:
        return "FAIL TO PARSE PROTO: %s\n%s" % (errmsg, util.toVisualHex(nData))
    
    port = getPort(nData)
    callback = __PORT_CALLBACK_DICT.get(port)
    if callback:
        return callback(nData)
    
    return "UNKNOWN PORT %d " % port
    
def __getSCTPPakcetBuff(pbBuff):
    size = len(pbBuff)
    checksum = size & 0xff
    for ch in pbBuff:
        checksum = (checksum + struct.unpack("B", ch)[0]) & 0xff
        
    return "\xAA\xBB\xCC" + "\x00" + struct.pack("B", size) + pbBuff + struct.pack("B", checksum)
    
def getDataToSendByJson(jsonstr):
    ctrlpb = getMyPbObj()
    if not ctrlpb:
        return False, "ERROR TO GET PB OBJECT from %s" % config.PB_SOURCE_FILE
        
    try:
        msg = pbjson.json2pb(ctrlpb.ControlMessage, jsonstr)
        return True, __getSCTPPakcetBuff(msg.SerializeToString())
        
    except Exception as e:
        return False, "JSON ERROR: %s" % e.__str__()
        