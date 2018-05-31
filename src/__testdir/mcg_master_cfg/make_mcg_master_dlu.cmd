@echo off
setlocal enabledelayedexpansion

if exist ..\..\ansi.txt echo [1;33m
echo ==========================================
echo    Processing: MCG Master Configuration  
echo ==========================================
if exist ..\..\ansi.txt echo [1;32m


if NOT "%1"=="" (
	set BUILD_DOTTED=%1
	goto splitversion
) else if NOT "%VERSION_DOTTED%"=="" goto makedlu

:setversion
set /p BUILD_DOTTED="Enter full MCG Master Configuration version (V.R.U.E): "


:splitversion
for /f "tokens=1-4 delims=." %%a in ("%BUILD_DOTTED: by=.%") do (
	set V_VERSION=%%a
	set R_VERSION=%%b
	set U_VERSION=%%c
	set E_VERSION=%%d
)

:checkversion
if "%V_VERSION%"=="" (
	echo Invalid version. Retry again.
	goto setversion
) else if "%R_VERSION%"=="" (
	echo Invalid release. Retry again.
	goto setversion
) else if "%U_VERSION%"=="" (
	echo Invalid Update. Retry again.
	goto setversion
) else if "%E_VERSION%"=="" (
	echo Invalid Evolution. Retry again.
	goto setversion
)

set VERSION_FULL=%V_VERSION%%R_VERSION%%U_VERSION%0
set VERSION_DOTTED=%V_VERSION%.%R_VERSION%.%U_VERSION%.0
set BUILD_VERSION=%V_VERSION%%R_VERSION%%U_VERSION%%E_VERSION%
set BUILD_DOTTED=%V_VERSION%.%R_VERSION%.%U_VERSION%.%E_VERSION%

:makedlu
set OLDPATH=%PATH%
set PATH=.;%OLDPATH%

rem validate file
..\..\01_bin\xmlvalidator mcg_master.xml cmconfiguration.xsd
if errorlevel 0 (
    echo Making MCG_MASTER DLU ...
    ..\..\01_bin\makedlu.exe mcg_master.xml MCG_MASTER %VERSION_DOTTED% DLU_TYPE_MASTER_COMPONENT META Type:c;Supplier:BT;ProductID:- OUTFILE MCG_MASTER.dl2 >NUL
    
) else (
    echo.
    color 47
    ..\..\01_bin\play_error.cmd
    echo mcg_master.xml file is invalid! Please check.
    echo .
    echo Failed to build DLU.
    pause
    color
)

rem validate file
..\..\01_bin\xmlvalidator mcg_master_with_optional_comp.xml cmconfiguration.xsd
if errorlevel 0 (
    echo Making MCG_MASTER_WITH_OPTIONAL_COMP DLU ...
    ..\..\01_bin\makedlu.exe mcg_master_with_optional_comp.xml MCG_MASTER_WITH_OPTIONAL_COMP %VERSION_DOTTED% DLU_TYPE_MASTER_COMPONENT META Type:c;Supplier:BT;ProductID:- OUTFILE MCG_MASTER_WITH_OPTIONAL_COMP.dl2 >NUL
    
) else (
    echo.
    color 47
    ..\..\01_bin\play_error.cmd
    echo mcg_master_with_optional_comp.xml file is invalid! Please check.
    echo .
    echo Failed to build DLU.
    pause
    color
)

set PATH=%OLDPATH%

echo.
echo ... done!
if exist ..\..\ansi.txt echo [1;33m
echo ==========================================
if exist ..\..\ansi.txt echo [0m
echo.
