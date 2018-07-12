@echo off
setlocal enabledelayedexpansion

set FILE_PATH=%~dp0
set LOCAL_DIR=%FILE_PATH:~0,-1%

cls
call enableansi.cmd

if "%ANSI_SET%"=="Y" (
    echo [2J
    echo [1;33m
)
echo =====================================================================
echo ' Copying MGC Release from GBE Repository to QNAP MCG Test Software '
echo =====================================================================
if "%ANSI_SET%"=="Y" (
    echo [1;32m
)
set CWD=%CD%

set USERNAME=tburri
set PASSWORD=

set REMOTE_VERSION=
set LOCAL_VERSION1=
set QNAP_DRIVE_LETTER=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-h" goto error
if "%~1"=="--help" goto error
if "%~1"=="-s" (
	if "%~2"=="" goto error
	set REMOTE_VERSION=%~2
	shift
) else if "%~1"=="-d" (
	if "%~2"=="" goto error
	set LOCAL_VERSION1=%~2
	shift
) else if "%~1"=="-driveletter" (
	if "%~2"=="" goto error
	set QNAP_DRIVE_LETTER=%~2
	shift
) else if "%~1"=="-p" (
	if "%~2"=="" goto error
	set PASSWORD=%~2
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
	set /p REMOTE_VERSION="Enter version on GBE Repository (3er base version v.r.u.e): "
)

if "%LOCAL_VERSION1%"=="" (
	set /p LOCAL_VERSION1="Enter version on QNAP MCG Test Software (3er base version v.r.u[.e]): "
)

if "%PASSWORD%"=="" (
	set /p PASSWORD="Enter GBE password for user %USERNAME%: "
)

REM call copy-mcg-product.cmd
start "Copying MCG Product to Test Environment" %LOCAL_DIR%\copy-mcg-product.cmd -s %REMOTE_VERSION% -d %LOCAL_VERSION1% -u %USERNAME% -p %PASSWORD% -driveletter %QNAP_DRIVE_LETTER%

REM call copy-mcg-firmware.cmd
start "Copying MCG Product to Test Environment" /wait %LOCAL_DIR%\copy-mcg-firmware.cmd -s %REMOTE_VERSION% -d %LOCAL_VERSION1% -u %USERNAME% -p %PASSWORD%

goto end


:error
echo "Wrong or missing parameter"
echo "Usage:"
echo "copy-mcg-release.cmd [-s V.R.U.E] -d V.R.U[.E] [-driveletter <QNAP Drive Letter>]"
echo.
echo "Copy MCG Release from remote (source) to QNAP MCG Test Sofware (destination)"
echo "V is always the base version (3), 4 and 5 are build automatically"

:end

echo ... done!
if "%ANSI_SET%"=="Y" (
    echo [1;33m
)
echo ===========================================================================
if "%ANSI_SET%"=="Y" (
    echo [0m
)
cd %CWD%
