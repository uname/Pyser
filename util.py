#-*- coding: utf-8 -*-
import os
import config
from binascii import hexlify, unhexlify
        
def checkData(data, _type):
    if data == '':
        return False, u"数据不能为空"

    errch, msg = None, "success"
    if _type == config.HEX_TYPE:
        data = ''.join(data.split())
        if len(data) % 2 != 0:
            errch, msg = True, u"HEX模式下，数据长度必须为偶数"
        else:
            for ch in data.upper():
                if not ('0' <= ch <= '9' or 'A' <= ch <= 'F'):
                    errch, msg = ch, u"数据中含有非法的HEX字符"
                    break
    elif _type == config.PROTO_TYPE:
        pass
    
    elif _type == config.ASCII_TYPE:
        pass
    
    else:
        errch = True
                    
    return not errch, msg

def __safeRead(filePath):
    try:
        return open(filePath, "r").read()
    except Exception as e:
        print e
        
def writeToFile(filePath, content):
    try:
        fp = open(filePath, "w")
        fp.write(content)
        fp.close()
        return True
    except:
        return False
          
def __readlParseTemplConfig(lines):
    templdict = {}
    tmplist = []
    protoKey = ""
    
    for line in lines:
        _line = line.strip()
        if _line == "":
            continue
        
        if _line.startswith("$"):
            if protoKey != "":
                templdict[protoKey] = "".join(tmplist)
                tmplist = []
            protoKey = _line[1:]
            
        else:
            tmplist.append(line + "\n")
            
    return templdict, "OK"
    
def parseTemplConfig(filePath):
    assert(isinstance(filePath, basestring))
    
    if not os.path.exists(filePath):
        return None, "config file not exists"
    
    content = __safeRead(filePath)
    if not content:
        return None, "read config file error"
    
    return __readlParseTemplConfig(content.split("\n"))
    
toVisualHex = lambda data: ' '.join([hexlify(c) for c in data]).upper()
toHex = lambda data: ''.join([unhexlify(data[i:i+2]) for i in xrange(0, len(data), 2)])
QStringToStr = lambda qstr : qstr.toUtf8().data()


