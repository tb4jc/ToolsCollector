@echo off
setlocal enabledelayedexpansion

set FILE_PATH=%~dp0
set LOCAL_DIR=%FILE_PATH:~0,-1%

set PSCP_BIN=%LOCAL_DIR%\..\99_Tools\network\PSCP.EXE

cls
call enableansi.cmd

if "%ANSI_SET%"=="Y" (
    echo [2J
    echo [1;33m
)
echo ============================================================================
echo ' Copying MGC Firmware build from GBE Repository to QNAP MCG Test Software '
echo ============================================================================
if "%ANSI_SET%"=="Y" (
    echo [1;32m
)
set CWD=%CD%

set USERNAME=tburri
set GBE_PASSW=

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
) else if "%~1"=="-p" (
	if "%~2"=="" goto error
	set GBE_PASSW=%~2
	shift
) else if "%~1"=="-u" (
	if "%~2"=="" goto error
	set USERNAME=%~2
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

if "%GBE_PASSW%"=="" (
	for /f "delims=" %%A in ('c:\myprogs\Dev\Python27x32\python.exe  -c "import getpass; print(getpass.getpass('Enter GBE GBE_PASSW for user %USERNAME%: '));"') do @set GBE_PASSW=%%A
    REM set /p GBE_PASSW="Enter GBE Password for user %USERNAME%: "
)

set LOCAL_VERSION2=4.%LOCAL_VERSION:~2,15%
set LOCAL_VERSION4=5.%LOCAL_VERSION:~2,15%
echo Version NRTOS2 %LOCAL_VERSION2%
echo Version NRTOS4 %LOCAL_VERSION4%


echo Coyping now version MCG Firmware build %REMOTE_VERSION% from GBE repository to QNAP MCG Test Software Version %LOCAL_VERSION% / %LOCAL_VERSION2% ...

set REMOTE_PATH=%USERNAME%@files.scan.bombardier.com:/opt/repository/components/mcg_firmware/%REMOTE_VERSION%

REM copy first NRTOS 1 build
set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION%
if not exist %LOCAL_PATH%\03_mcg_firmware (
	mkdir %LOCAL_PATH%\03_mcg_firmware
)

echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg/* %LOCAL_PATH%\03_mcg_firmware 
%PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg/* %LOCAL_PATH%\03_mcg_firmware 
echo.

REM 2018-03-22 no 3rd party DLUs anymore

REM copy NRTOS 2 build - after manipulating LOCAL_VERSION
set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION2%
if not exist %LOCAL_PATH%\03_mcg_firmware (
	mkdir %LOCAL_PATH%\03_mcg_firmware
)
echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg2/* %LOCAL_PATH%\03_mcg_firmware 
%PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg2/* %LOCAL_PATH%\03_mcg_firmware 
echo.

REM 2018-03-22 no 3rd party DLUs anymore

REM copy NRTOS 4 build - after manipulating LOCAL_VERSION
set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION4%
if not exist %LOCAL_PATH%\03_mcg_firmware (
	mkdir %LOCAL_PATH%\03_mcg_firmware
)
echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/nrtos4/* %LOCAL_PATH%\03_mcg_firmware 
%PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/nrtos4/* %LOCAL_PATH%\03_mcg_firmware 
echo.

goto end

:error
echo "Wrong or missing parameter"
echo "Usage:"
echo "copy-build-from-rep-to-install-loc.cmd [-s V.R.U.E] [-d V.R.U[.E]]"
echo.
echo "Copy MCG Firmware from remote (source) to QNAP MCG Test Sofware (destination)"

:end

echo ... done!
if "%ANSI_SET%"=="Y" (
    echo [1;33m
)
echo ============================================================================
if "%ANSI_SET%"=="Y" (
    echo [0m
)
cd %CWD%
