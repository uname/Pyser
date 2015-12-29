#-*- coding: utf-8 -*-
import config
import util

def __getVisualizedData_HEX(nData):
    return util.toVisualHex(nData)
    
def __getVisualizedData_ASCII(nData):
    return nData
    
__RECV_TYPE_HANDLE_DICT = { config.HEX_TYPE: __getVisualizedData_HEX, 
                            config.ASCII_TYPE: __getVisualizedData_ASCII }

def getDataToSend(hData, _type, asciiTail=""):
    """从本地数据和发送类型获取需要发送的数据"""
    data = "SYS-ERROR"
    ret = True
    if _type == config.HEX_TYPE:
        data = util.toHex(''.join(hData.split()))
    elif _type == config.ASCII_TYPE:
        data = hData + asciiTail
    
    return ret, data
    
def getVisualizedData(nData, _type):
    """根据接收类型获取网络数据的可视化数据"""
   
    data = "SYS-ERROR"
    if not isinstance(_type, basestring):
        return data
    
    handle = __RECV_TYPE_HANDLE_DICT.get(_type)
    if handle is None:
        return data
    
    return handle(nData)
