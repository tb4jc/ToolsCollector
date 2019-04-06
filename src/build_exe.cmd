@echo off
rem build standalone application with pyinstaller

REM call to build one single application and copying the required files afterwards
pyinstaller ^
--noconfirm ^
--clean ^
-n ToolsCollector ^
-p c:\Users\Thomas\Development\python\ToolsCollector\src\releasescripts ^
REM --add-data mainwindow.ui;. ^
REM --add-data toolsCollector.ini;. ^
REM --add-data batch_files;batch_files ^
--noconsole ^
-F ^
toolscollector.py

REM copy the ui file to the distribution
cp mainwindow.ui dist\.

REM copy the ini file to the distribution
if exist toolscollector.ini (
	cp toolscollector.ini dist\.
)

REM copy the batch files to the distribution
cp -
REM --add-data batch_files;batch_files ^
