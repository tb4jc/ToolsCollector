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
echo ===========================================================================
echo ' Copying MGC Product build from GBE Repository to QNAP MCG Test Software '
echo ===========================================================================
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


set REMOTE_VERSION1=%REMOTE_VERSION%
set REMOTE_VERSION2=4.%REMOTE_VERSION:~2%
set REMOTE_VERSION4=5.%REMOTE_VERSION:~2%
echo BUILD NRTOS1  %REMOTE_VERSION1%
echo BUILD NRTOS2  %REMOTE_VERSION2%
echo BUILD NRTOS4  %REMOTE_VERSION4%

set LOCAL_VERSION2=4.%LOCAL_VERSION1:~2%
set LOCAL_VERSION4=5.%LOCAL_VERSION1:~2%
echo Version NRTOS1 %LOCAL_VERSION1%
echo Version NRTOS2 %LOCAL_VERSION2%
echo Version NRTOS4 %LOCAL_VERSION4%

echo Coyping now OS Base, Middleware and Config from MCG Product build %REMOTE_VERSION1%, %REMOTE_VERSION2% and %REMOTE_VERSION4% from GBE repository to QNAP MCG Test Software Version %LOCAL_VERSION1% / %LOCAL_VERSION2% / %LOCAL_VERSION4% ...

set TEST_ENV_SW_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG
set CFG_BIN_PATH=%TEST_ENV_SW_PATH%\01_Configurations\01_bin
set CFG_TESTS_PATH=%TEST_ENV_SW_PATH%\01_Configurations\20_tests

REM copy first NRTOS 1 build
set REMOTE_PATH=%USERNAME%@files.scan.bombardier.com:/opt/repository/products/mcg/%REMOTE_VERSION1%/delivery

set LOCAL_PATH=%TEST_ENV_SW_PATH%\%LOCAL_VERSION1%
if not exist %LOCAL_PATH%\01_os_base (
	mkdir %LOCAL_PATH%\01_os_base   
)
if not exist %LOCAL_PATH%\02_middleware (
	mkdir %LOCAL_PATH%\02_middleware
)
if not exist %LOCAL_PATH%\04_cfg (
	mkdir %LOCAL_PATH%\04_cfg\01_bin
)
if not exist %LOCAL_PATH%\04_cfg\20_tests (
	mkdir %LOCAL_PATH%\04_cfg\20_tests
)

echo.
echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/01_os_base/* %LOCAL_PATH%\01_os_base 
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/01_os_base/* %LOCAL_PATH%\01_os_base 
echo.

echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/02_middleware/* %LOCAL_PATH%\02_middleware 
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/02_middleware/* %LOCAL_PATH%\02_middleware 
echo.

echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/04_cfg/* %LOCAL_PATH%\04_cfg
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/04_cfg/* %LOCAL_PATH%\04_cfg
echo.

echo copy %TEST_ENV_SW_PATH%\00_mcp\MCG_Platform_nrtos1.mdl %LOCAL_PATH%\MCG_Platform.mdl /Y
copy %TEST_ENV_SW_PATH%\00_mcp\MCG_Platform_nrtos1.mdl %LOCAL_PATH%\MCG_Platform.mdl /Y
echo.

echo "xcopy %CFG_BIN_PATH%\*              %LOCAL_PATH%\04_cfg\01_bin /E /F /Y"
xcopy       %CFG_BIN_PATH%\*              %LOCAL_PATH%\04_cfg\01_bin /E /F /Y
echo.

echo "xcopy %CFG_TESTS_PATH%\*            %LOCAL_PATH%\04_cfg\20_tests /E /F /Y"
xcopy       %CFG_TESTS_PATH%\*            %LOCAL_PATH%\04_cfg\20_tests /E /F /Y

if "%QNAP_DRIVE_LETTER%"=="" (
    echo Drive letter of QNAP attaching not given - calling configuration build script skipped
) else (
    echo Executing configuration builder
    start "Build configuration DLUs for release %REMOTE_VERSION1%" "%QNAP_DRIVE_LETTER%:\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION1%\04_cfg\20_tests\Execute_TestCases.cmd" -buildonly -v %REMOTE_VERSION1%
)

REM copy NRTOS 2 build - after manipulating LOCAL_VERSION
set REMOTE_PATH=%USERNAME%@files.scan.bombardier.com:/opt/repository/products/mcg/%REMOTE_VERSION2%/delivery
set LOCAL_PATH=%TEST_ENV_SW_PATH%\%LOCAL_VERSION2%
if not exist %LOCAL_PATH%\01_os_base (
	mkdir %LOCAL_PATH%\01_os_base
)
if not exist %LOCAL_PATH%\02_middleware (
	mkdir %LOCAL_PATH%\02_middleware
)
if not exist %LOCAL_PATH%\04_cfg (
	mkdir %LOCAL_PATH%\04_cfg\01_bin
)
if not exist %LOCAL_PATH%\04_cfg\20_tests (
	mkdir %LOCAL_PATH%\04_cfg\20_tests
)

echo.
echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/01_os_base/* %LOCAL_PATH%\01_os_base 
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/01_os_base/* %LOCAL_PATH%\01_os_base 
echo.

echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/02_middleware/* %LOCAL_PATH%\02_middleware 
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/02_middleware/* %LOCAL_PATH%\02_middleware 
echo.

echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/04_cfg/* %LOCAL_PATH%\04_cfg
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/04_cfg/* %LOCAL_PATH%\04_cfg
echo.

echo copy %TEST_ENV_SW_PATH%\00_mcp\MCG_Platform_nrtos2.mdl %LOCAL_PATH%\MCG_Platform.mdl /Y
copy %TEST_ENV_SW_PATH%\00_mcp\MCG_Platform_nrtos2.mdl %LOCAL_PATH%\MCG_Platform.mdl /Y
echo.

echo "xcopy %CFG_BIN_PATH%\*              %LOCAL_PATH%\04_cfg\01_bin /E /F /Y"
xcopy       %CFG_BIN_PATH%\*              %LOCAL_PATH%\04_cfg\01_bin /E /F /Y

echo.
echo "xcopy %CFG_TESTS_PATH%\*            %LOCAL_PATH%\04_cfg\20_tests /E /F /Y"
xcopy       %CFG_TESTS_PATH%\*            %LOCAL_PATH%\04_cfg\20_tests /E /F /Y

if "%QNAP_DRIVE_LETTER%"=="" (
    echo Drive letter of QNAP attaching not given - calling configuration build script skipped
) else (
    echo Executing configuration builder
    start "Build configuration DLUs for release %REMOTE_VERSION2%"  "%QNAP_DRIVE_LETTER%:\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION2%\04_cfg\20_tests\Execute_TestCases.cmd" -buildonly -v %REMOTE_VERSION2%
)

REM copy NRTOS 4 build - after manipulating LOCAL_VERSION
set REMOTE_PATH=%USERNAME%@files.scan.bombardier.com:/opt/repository/products/mcg/%REMOTE_VERSION4%/delivery
set LOCAL_PATH=%TEST_ENV_SW_PATH%\%LOCAL_VERSION4%
if not exist %LOCAL_PATH%\01_os_base (
	mkdir %LOCAL_PATH%\01_os_base
)
if not exist %LOCAL_PATH%\02_middleware (
	mkdir %LOCAL_PATH%\02_middleware
)
if not exist %LOCAL_PATH%\04_cfg (
	mkdir %LOCAL_PATH%\04_cfg\01_bin
)
if not exist %LOCAL_PATH%\04_cfg\20_tests (
	mkdir %LOCAL_PATH%\04_cfg\20_tests
)

echo.
echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/01_os_base/* %LOCAL_PATH%\01_os_base 
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/01_os_base/* %LOCAL_PATH%\01_os_base 
echo.

echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/02_middleware/* %LOCAL_PATH%\02_middleware 
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/02_middleware/* %LOCAL_PATH%\02_middleware 
echo.

echo %PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/04_cfg/* %LOCAL_PATH%\04_cfg
%PSCP_BIN% -r -pw %PASSWORD% %REMOTE_PATH%/04_cfg/* %LOCAL_PATH%\04_cfg
echo.

echo copy %TEST_ENV_SW_PATH%\00_mcp\MCG_Platform_nrtos4.mdl %LOCAL_PATH%\MCG_Platform.mdl /Y
copy %TEST_ENV_SW_PATH%\00_mcp\MCG_Platform_nrtos4.mdl %LOCAL_PATH%\MCG_Platform.mdl /Y
echo.

echo "xcopy %CFG_BIN_PATH%\*              %LOCAL_PATH%\04_cfg\01_bin /E /F /Y"
xcopy       %CFG_BIN_PATH%\*              %LOCAL_PATH%\04_cfg\01_bin /E /F /Y
echo.

echo "xcopy %CFG_TESTS_PATH%\*            %LOCAL_PATH%\04_cfg\20_tests /E /F /Y"
xcopy       %CFG_TESTS_PATH%\*            %LOCAL_PATH%\04_cfg\20_tests /E /F /Y

if "%QNAP_DRIVE_LETTER%"=="" (
    echo Drive letter of QNAP attaching not given - calling configuration build script skipped
) else (
    echo Executing configuration builder
    start "Build configuration DLUs for release %REMOTE_VERSION4%" "%QNAP_DRIVE_LETTER%:\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION4%\04_cfg\20_tests\Execute_TestCases.cmd" -buildonly -v %REMOTE_VERSION4%
)

goto end


:error
echo "Wrong or missing parameter"
echo "Usage:"
echo "copy-mcg-product-build-from-rep-to-install-loc.cmd [-s V.R.U.E] -d V.R.U[.E] [-driveletter <QNAP Drive Letter>]"
echo.
echo "Copy MCG Product from remote (source) to QNAP MCG Test Sofware (destination)"
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
