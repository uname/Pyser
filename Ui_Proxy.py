#-*- coding: utf-8 -*-
from Ui_MainWindow import Ui_MainWindow
from PyQt4.QtGui import QKeySequence, QIcon, QPixmap
from PyQt4.QtCore import Qt, SIGNAL, QTime, QString
from Serial import Serial
import util
import config


class Ui_Proxy(Ui_MainWindow):

    def __init__(self, parent=None):
        Ui_MainWindow.__init__(self)
    
    def setupWidget(self, wobj):
        wobj.setWindowIcon(QIcon(QPixmap(":/app/icons/app/logo.png")))
        self.updatePortComBox(isOpening=True)
        self.send_pushButton.setShortcut(QKeySequence(Qt.Key_Return + Qt.CTRL))
        
        self.initByConfig()
        
        self.onSendTypeChanged()
        
        self.send_pushButton.setEnabled(False)
        
        self.comSettingsWidgets = ( \
            self.port_comboBox, self.baud_comboBox,
            self.parity_comboBox, self.bytesize_comboBox,
            self.stopbits_comboBox )
    
    def updatePortComBox(self, isOpening=False):
        """ 更新串口列表, 暂不删除已不存在的端口
        若没有已打开的串口则将最新发现的串口设置为当前串口
        """
        newCount = 0
        for port in Serial.getActivePorts():
            if self.port_comboBox.findText(port) > -1:
                continue
            self.port_comboBox.addItem(port)
            newCount += 1
        
        if newCount == 0:
            return 0
            
        if not isOpening:
            lastIndex = self.port_comboBox.count() - 1
            if lastIndex > -1:
                self.port_comboBox.setCurrentIndex(lastIndex)
        
        return newCount
    
    def initByConfig(self):
        configDict = config.getConfigDict()
        try:
            self.setCOMSettings(configDict.get(config.COMSETTINGS_KEY))
            self.setRecvSettings(configDict.get(config.RECVSETTINGS_KEY))
            self.setSendSettings(configDict.get(config.SENDSETTINGS_KEY))
        except Exception as e:
            print e
        
    def setCOMSettings(self, comSettings):
        if not isinstance(comSettings, dict):
            return
            
        port = comSettings.get(config.PORT_KEY, "").upper()
        if port != "":
            self.setIndexIfFound(self.port_comboBox, str(port))
        
        baud = comSettings.get(config.BAUD_KEY, config.DEFAULT_BAUD)
        self.setIndexIfFound(self.baud_comboBox, str(baud))
        
        bytesize = comSettings.get(config.BYTESIZE_KEY, config.DEFAULT_BYTESIZE)
        self.setIndexIfFound(self.baud_comboBox, str(bytesize))
        
        parity = comSettings.get(config.PARITY_KEY, config.DEFAULT_PARTITY)
        self.setIndexIfFound(self.parity_comboBox, parity)
        
        stopbits = comSettings.get(config.STOPBITS_KEY, config.DEFAULT_STOPBITS)
        self.setIndexIfFound(self.stopbits_comboBox, str(stopbits))
        
    def setRecvSettings(self, recvSettings):
        if not isinstance(recvSettings, dict):
            return
            
        recvtype = recvSettings.get(config.RECVTYPE_KEY, config.ASCII_TYPE)
        self.setIndexIfFound(self.recvType_comboBox, recvtype)
        
        autolinefeed = recvSettings.get(config.AUTOLINEFEED_KEY, config.DEFAULT_AUTOLINEFEED).upper()
        self.autoLF_checkBox.setChecked(autolinefeed == config.YES)
        
        hidersflag = recvSettings.get(config.HIDERSFLAG_KEY, config.DEFAULT_HIDERSFLAG).upper()
        self.hideSRFlag_checkBox.setChecked(hidersflag == config.YES)
        
    def setSendSettings(self, sendSettings):
        if not isinstance(sendSettings, dict):
            return
            
        sendtype = sendSettings.get(config.SENDTYPE_KEY, config.ASCII_TYPE)
        self.setIndexIfFound(self.sendType_comboBox, sendtype)
        
        clearsenttext = sendSettings.get(config.CLEARSENTTEXT_KEY, config.DEFAULT_CLEARSENTTEXT).upper()
        self.clearSentText_checkBox.setChecked(clearsenttext == config.YES)

        showsent = sendSettings.get(config.SHOWSENT_KEY, config.DEFAULT_SHOWSENT).upper()
        self.showSent_checkBox.setChecked(showsent == config.YES)
        
        sendinterval = sendSettings.get(config.SENDINTERVAL_KEY, config.DEFAULT_SHOWSENT)
        self.sendInterval_spinBox.setValue(int(sendinterval))
    
    def getCurrentConfigDict(self):
        configDict = {config.COMSETTINGS_KEY : {}, config.RECVSETTINGS_KEY: {}, config.SENDSETTINGS_KEY: {}}
        configDict[config.COMSETTINGS_KEY][config.PORT_KEY] = util.QStringToStr(self.port_comboBox.currentText())
        configDict[config.COMSETTINGS_KEY][config.BAUD_KEY] = util.QStringToStr(self.baud_comboBox.currentText())
        configDict[config.COMSETTINGS_KEY][config.BYTESIZE_KEY] = util.QStringToStr(self.bytesize_comboBox.currentText())
        configDict[config.COMSETTINGS_KEY][config.PARITY_KEY] = util.QStringToStr(self.parity_comboBox.currentText())
        configDict[config.COMSETTINGS_KEY][config.STOPBITS_KEY] = util.QStringToStr(self.stopbits_comboBox.currentText())
        
        configDict[config.RECVSETTINGS_KEY][config.RECVTYPE_KEY] = util.QStringToStr(self.recvType_comboBox.currentText())
        configDict[config.RECVSETTINGS_KEY][config.AUTOLINEFEED_KEY] = self.autoLF_checkBox.isChecked() and config.YES or config.NO
        configDict[config.RECVSETTINGS_KEY][config.HIDERSFLAG_KEY] = self.hideSRFlag_checkBox.isChecked() and config.YES or config.NO
        configDict[config.RECVSETTINGS_KEY][config.MERGE_INTERVAL_KEY] = config.mergeInterval
        
        configDict[config.SENDSETTINGS_KEY][config.SENDTYPE_KEY] = util.QStringToStr(self.sendType_comboBox.currentText())
        configDict[config.SENDSETTINGS_KEY][config.CLEARSENTTEXT_KEY] = self.clearSentText_checkBox.isChecked() and config.YES or config.NO
        configDict[config.SENDSETTINGS_KEY][config.SHOWSENT_KEY] = self.showSent_checkBox.isChecked() and config.YES or config.NO
        configDict[config.SENDSETTINGS_KEY][config.SENDINTERVAL_KEY] = str(self.sendInterval_spinBox.value())
        
        return configDict
        
    def setIndexIfFound(self, combox, text):
        index = combox.findText(text)
        if index > -1:
            combox.setCurrentIndex(index)
    
    def addRXBytesNumber(self, num=0):
        self.rx_lcdNumber.display(num + self.rx_lcdNumber.intValue())
    
    def addTXBytesNumber(self, num=0):
        self.tx_lcdNumber.display(num + self.tx_lcdNumber.intValue())
        
    def clearLcdNumber(self):
        self.rx_lcdNumber.display(0)
        self.tx_lcdNumber.display(0)
    
    def getPortSettings(self):
        comPort = util.QStringToStr(self.port_comboBox.currentText())
        baud = int(util.QStringToStr(self.baud_comboBox.currentText()))
        parity = Serial.PARITIES[self.parity_comboBox.currentIndex()]
        bytesize = Serial.BYTESIZES[self.bytesize_comboBox.currentIndex()]
        stopbits = Serial.STOPBITSES[self.stopbits_comboBox.currentIndex()]
        
        return  {
            "port": comPort, "baund": baud, "bytesize": bytesize,
            "parity": parity, "stopbits": stopbits, "timeout": 1
        }
    
    def getDataAndType(self):
        return self.send_TextEdit.toPlainText().toUtf8().data(), \
                  config.SEND_DATA_TYPES[self.sendType_comboBox.currentIndex()]
        
    def onPortOpened(self):
        self.open_pushButton.setText(u"关闭")
        self.open_pushButton.setStyleSheet("background-color: rgb(85, 255, 0);")
        self.setComSettingsEnabled(False)
        self.send_pushButton.setEnabled(True)
    
    def setComSettingsEnabled(self, enable):
        map(lambda widget: widget.setEnabled(enable), self.comSettingsWidgets)
        
    def onPortOpening(self):
        pass
    
    def onPortClosed(self):
        self.open_pushButton.setText(u"打开")
        self.open_pushButton.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.setComSettingsEnabled(True)
        self.send_pushButton.setEnabled(False)
    
    def onSendData(self, data, _type=config.ASCII_TYPE):
        if self.clearSentText_checkBox.isChecked() and not self.autoSend_checkBox.isChecked():
            self.send_TextEdit.clear()
            
        if not self.showSent_checkBox.isChecked():
            return
            
        text = data
        if not self.hideSRFlag_checkBox.isChecked():
            text = 'SEND (%s)\n%s\n' % (util.QStringToStr(QTime.currentTime().toString()), data)
            
        self.recv_TextBrowser.setPlainTextWithNoNL(text)

    
    def onRecvData(self, data):
        text = data
        if not self.hideSRFlag_checkBox.isChecked():
            text = 'RECV (%s)\n%s' % (util.QStringToStr(QTime.currentTime().toString()), data)
        
        self.recv_TextBrowser.setPlainTextWithNoNL(text)
        
        if self.autoLF_checkBox.isChecked():
            self.recv_TextBrowser.setPlainTextWithNoNL("\n")
    
    def clearHistory(self):
        self.recv_TextBrowser.clear()
    
    def getRecvType(self):
        return config.RECV_DATA_TYPES[self.recvType_comboBox.currentIndex()]
    
    def getSendType(self):
        return config.SEND_DATA_TYPES[self.sendType_comboBox.currentIndex()]
    
    def getAsciiTail(self):
        return config.ASCII_TAIL[self.asciiTail_comboBox.currentIndex()]
        
    def onAutoSend(self, status):
        if status == 0:   #Unchecked
            self.send_pushButton.setText(u"发送")
            self.send_pushButton.setEnabled(True)
            self.send_TextEdit.setEnabled(True)
            
        elif status == 2: #Checked
            self.send_pushButton.setText(u"开始自动发送")
    
    def onAutoSendStarted(self):
        self.send_pushButton.setEnabled(False)
        self.send_TextEdit.setEnabled(False)
        
    def getAutoSendInterval(self):
        return self.sendInterval_spinBox.value()
        
    def updateAutoSendTimes(self, times):
        self.send_pushButton.setText(u"已自动发送 %03d 次" % times)

        
    def onProtoTemplSelected(self, templJson):
        self.send_TextEdit.setText(templJson)
        
    def onSendTypeChanged(self):
        sendType = self.getSendType()
        self.asciiTail_comboBox.setEnabled(sendType == config.ASCII_TYPE)
        self.inc_checkBox.setEnabled(sendType == config.ASCII_TYPE)
        self.resetStartVal_pushButton.setEnabled(sendType == config.ASCII_TYPE)
        
    def getRecvWidgetContent(self):
        return self.recv_TextBrowser.toPlainText().toUtf8().data()
        