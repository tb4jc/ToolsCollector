@echo off
setlocal enabledelayedexpansion

set FILE_PATH=%~dp0
set LOCAL_DIR=%FILE_PATH:~0,-1%

cls
call enableansi.cmd

echo [2J
echo [1;33m
echo ============================================================================
echo ' Copying MGC Firmware build from GBE Repository to QNAP MCG Test Software '
echo ============================================================================
echo [1;32m
set CWD=%CD%

set REMOTE_VERSION=
set LOCAL_VERSION=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-s" (
	if "%~2"=="" goto error
	set REMOTE_VERSION=%~2
	shift
) else if "%~1"=="-d" (
	if "%~2"=="" goto error
	set LOCAL_VERSION=%~2
	shift
) else (
	goto error
)
shift
goto parse
:endparse

if "%REMOTE_VERSION%"=="" (
	set /p REMOTE_VERSION="Enter version on GBE Repository: "
)

if "%LOCAL_VERSION%"=="" (
	set /p LOCAL_VERSION="Enter version on QNAP MCG Test Software: "
)

set LOCAL_VERSION2=4.%LOCAL_VERSION:~2,15%
set LOCAL_VERSION4=5.%LOCAL_VERSION:~2,15%
echo Version NRTOS2 %LOCAL_VERSION2%
echo Version NRTOS4 %LOCAL_VERSION4%

echo Coyping now version MCG Firmware build %REMOTE_VERSION% from GBE repository to QNAP MCG Test Software Version %LOCAL_VERSION% / %LOCAL_VERSION2% ...

set REMOTE_PATH=\\files.scan.bombardier.com\repository\components\mcg_firmware\%REMOTE_VERSION%

REM copy first NRTOS 1 build
set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION%
if not exist %LOCAL_PATH%\03_mcg_firmware (
	mkdir %LOCAL_PATH%\03_mcg_firmware
)
if not exist %LOCAL_PATH%\06_3rd_party (
	mkdir %LOCAL_PATH%\06_3rd_party
)
echo "xcopy %REMOTE_PATH%\dlu\mcg\*  %LOCAL_PATH%\03_mcg_firmware /E /F /Y"
      xcopy %REMOTE_PATH%\dlu\mcg\*  %LOCAL_PATH%\03_mcg_firmware /E /F /Y

REM 2018-03-22 no 3rd party DLUs anymore
REM echo "mv %LOCAL_PATH%\03_mcg_firmware\3rd_party\*  %LOCAL_PATH%\06_3rd_party /Y"
      REM mv %LOCAL_PATH%\03_mcg_firmware\3rd_party\*  %LOCAL_PATH%\06_3rd_party /Y
REM echo "del %LOCAL_PATH%\03_mcg_firmware\3rd_party /S /F"
	  REM del %LOCAL_PATH%\03_mcg_firmware\3rd_party /S /F

REM copy NRTOS 2 build - after manipulating LOCAL_VERSION
set LOCAL_PATH2=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION2%
if not exist %LOCAL_PATH2%\03_mcg_firmware (
	mkdir %LOCAL_PATH2%\03_mcg_firmware
)
if not exist %LOCAL_PATH2%\06_3rd_party (
	mkdir %LOCAL_PATH2%\06_3rd_party
)
echo "xcopy %REMOTE_PATH%\dlu\mcg2\*  %LOCAL_PATH2%\03_mcg_firmware /E /F /Y"
      xcopy %REMOTE_PATH%\dlu\mcg2\*  %LOCAL_PATH2%\03_mcg_firmware /E /F /Y

REM 2018-03-22 no 3rd party DLUs anymore
REM echo "mv %LOCAL_PATH2%\03_mcg_firmware\3rd_party\*  %LOCAL_PATH2%\06_3rd_party /Y"
      REM mv %LOCAL_PATH2%\03_mcg_firmware\3rd_party\*  %LOCAL_PATH2%\06_3rd_party /Y
REM echo "del %LOCAL_PATH%\03_mcg_firmware\3rd_party /S /F"
	  REM del %LOCAL_PATH%\03_mcg_firmware\3rd_party /S /F

REM copy NRTOS 4 build - after manipulating LOCAL_VERSION
set LOCAL_PATH4=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION4%
if not exist %LOCAL_PATH4%\03_mcg_firmware (
	mkdir %LOCAL_PATH4%\03_mcg_firmware
)
echo "xcopy %REOTE_PATH%\dlu\nrtos4\*  %LOCAL_PATH4%\03_mcg_firmware /E /F /Y"
      xcopy %REMOTE_PATH%\dlu\nrtos4\*  %LOCAL_PATH4%\03_mcg_firmware /E /F /Y

goto end

:error
echo "Wrong or missing parameter"
echo "Usage:"
echo "copy-build-from-rep-to-install-loc.cmd [-s V.R.U.E] [-d V.R.U[.E]]"
echo
echo "Copy MCG Firmware from remote (source) to QNAP MCG Test Sofware (destination)"

:end

echo ... done!
echo [1;33m
echo ============================================================================
echo [0m
cd %CWD%
