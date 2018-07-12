@echo off
setlocal enabledelayedexpansion

if exist ..\..\ansi.txt echo [1;33m
echo ==============================================
echo  Create pack tag from branch
echo ==============================================
if exist ..\..\ansi.txt echo [1;32m


if "%1"=="" (
    set /p REPO_VERSION="Enter full MCG FW version (V.R.U.E) in GBE Repo: "
) else (
	set REPO_VERSION=%1
)

if "%2"=="" (
    set /p INST_DIR_NAME="Enter installation directory name (V.R.U.x or other): "
) else (
	set INST_DIR_NAME=%1
)

if "%3"=="" (
    set INST_DIR=c:\Users\Thomas\Development\python\ToolsCollector\src\__mcg_inst_dir
) else (
    set INST_DIR=%3
)

:copy_to_inst
set OLDPATH=%PATH%
set PATH=.;%OLDPATH%

echo "Called with option 1=%REPO_VERSION%, 2=%INST_DIR_NAME%, 3=%INST_DIR%"

set PATH=%OLDPATH%

echo.
echo ... done!
if exist ..\..\ansi.txt echo [1;33m
echo ==========================================
if exist ..\..\ansi.txt echo [0m
REM echo.

if "%1"=="1.2.3.4" exit 1
