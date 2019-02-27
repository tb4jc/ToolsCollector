@echo off
setlocal enabledelayedexpansion

if exist ..\..\ansi.txt echo [1;33m
echo ==============================================
echo  Create pack tags from branch
echo ==============================================
if exist ..\..\ansi.txt echo [1;32m


if "%1"=="" (
    set /p BRANCH_VERSION="Enter MCG Pack Branch version (V.R.U.E): "
) else (
	set BRANCH_VERSION=%1
)

if "%2"=="" (
    set /p TAG_VERSION_BASE="Enter MCG Pack Tag version (base 3.r.u.e) (V.R.U.E): "
) else (
	set TAG_VERSION_BASE=%1
)

:create_tags
set OLDPATH=%PATH%
set PATH=.;%OLDPATH%

echo "Called with option 1=%BRANCH_VERSION%, 2=%TAG_VERSION_BASE%"

set PATH=%OLDPATH%

echo.
echo ... done!
if exist ..\..\ansi.txt echo [1;33m
echo ==========================================
if exist ..\..\ansi.txt echo [0m
REM echo.

if "%1"=="1.2.3.4" exit 1
