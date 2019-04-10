@echo off
setlocal enabledelayedexpansion

if exist ..\..\ansi.txt echo [1;33m
echo ============================================================================
echo ' Copying MGC Firmware build from GBE Repository to QNAP MCG Test Software '
echo ============================================================================
if exist ..\..\ansi.txt echo [1;32m

set FILE_PATH=%~dp0
set LOCAL_DIR=%FILE_PATH:~0,-1%

set REPO_VERSION=
set LOCAL_VERSION=
set INST_DIR=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-s" (
	if "%~2"=="" goto error
	set REPO_VERSION=%~2
	shift
) else if "%~1"=="-d" (
	if "%~2"=="" goto error
	set LOCAL_VERSION=%~2
	shift
) else if "%~1"=="-p" (
	if "%~2"=="" goto error
	set INST_DIR=%~2
	shift
) else (
	goto error
)
shift
goto parse
:endparse


if "%REPO_VERSION%"=="" (
    set /p REPO_VERSION="Enter full MCG FW version (V.R.U.E) in GBE Repo: "
)

if "%LOCAL_VERSION%"=="" (
    set /p LOCAL_VERSION="Enter installation directory name (V.R.U.x or other): "
)

if "%INST_DIR%"=="" (
    set INST_DIR=c:\Users\Thomas\Development\python\ToolsCollector\src\__mcg_inst_dir
	REM set INST_DIR=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG
)

set LOCAL_VERSION2=4.%LOCAL_VERSION:~2,15%
set LOCAL_VERSION4=5.%LOCAL_VERSION:~2,15%
echo Version NRTOS1 %LOCAL_VERSION%
echo Version NRTOS2 %LOCAL_VERSION2%
echo Version NRTOS4 %LOCAL_VERSION4%

set OLDPATH=%PATH%
set PATH=.;%OLDPATH%

echo "Called with option 1=%REPO_VERSION%, 2=%LOCAL_VERSION%, 3=%INST_DIR%"
REM ===

echo Coyping now version MCG Firmware build %REPO_VERSION% from GBE repository to QNAP MCG Test Software '%INST_DIR%' with Version %LOCAL_VERSION% / %LOCAL_VERSION2% ...

set REMOTE_PATH=\\files.scan.bombardier.com\repository\components\mcg_firmware\%REPO_VERSION%

REM copy first NRTOS 1 build
set LOCAL_PATH=%INST_DIR%\%LOCAL_VERSION%
if not exist %LOCAL_PATH%\03_mcg_firmware (
	mkdir %LOCAL_PATH%\03_mcg_firmware
)
echo "xcopy %REMOTE_PATH%\dlu\mcg\* %LOCAL_PATH%\03_mcg_firmware /E /F /Y"
REM xcopy %REMOTE_PATH%\dlu\mcg\* %LOCAL_PATH%\03_mcg_firmware /E /F /Y

REM copy NRTOS 2 build - after manipulating LOCAL_VERSION
set LOCAL_PATH2=%INST_DIR%\%LOCAL_VERSION2%
if not exist %LOCAL_PATH2%\03_mcg_firmware (
	mkdir %LOCAL_PATH2%\03_mcg_firmware
)
echo "xcopy %REMOTE_PATH%\dlu\mcg2\* %LOCAL_PATH2%\03_mcg_firmware /E /F /Y"
REM xcopy %REMOTE_PATH%\dlu\mcg2\* %LOCAL_PATH2%\03_mcg_firmware /E /F /Y

REM copy NRTOS 4 build - after manipulating LOCAL_VERSION
set LOCAL_PATH4=%INST_DIR%\%LOCAL_VERSION4%
if not exist %LOCAL_PATH4%\03_mcg_firmware (
	mkdir %LOCAL_PATH4%\03_mcg_firmware
)
echo "xcopy %REOTE_PATH%\dlu\nrtos4\* %LOCAL_PATH4%\03_mcg_firmware /E /F /Y"
REM xcopy %REMOTE_PATH%\dlu\nrtos4\* %LOCAL_PATH4%\03_mcg_firmware /E /F /Y

set PATH=%OLDPATH%
goto end


:error
echo "Wrong or missing parameter"
echo "Usage:"
echo "copy-build-from-rep-to-install-loc.cmd [-s V.R.U.E] [-d V.R.U[.E]]"
echo
echo "Copy MCG Firmware from remote (source) to QNAP MCG Test Sofware (destination)"


:end
echo.
echo ... done!
if exist ..\..\ansi.txt echo [1;33m
echo ============================================================================
if exist ..\..\ansi.txt echo [0m
REM echo.

if "%REPO_VERSION%"=="1.2.3.4" exit 1
