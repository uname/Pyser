@echo off
genqrc.py
pyrcc4 -py2 tmp.qrc -o ../appicons.py
del tmp.qrc