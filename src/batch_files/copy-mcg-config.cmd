@echo off
setlocal enabledelayedexpansion

set FILE_PATH=%~dp0
set LOCAL_DIR=%FILE_PATH:~0,-1%
set FILENAME=%~n0%~x0

set PSCP_BIN=%LOCAL_DIR%\..\99_Tools\network\PSCP.EXE

cls
call enableansi.cmd

if "%ANSI_SET%"=="Y" (
    echo [2J
    echo [1;33m
)
echo ============================================================================
echo ' Copying MGC Config build from GBE Repository to QNAP MCG Test Software '
echo ============================================================================
if "%ANSI_SET%"=="Y" (
    echo [1;32m
)

set CWD=%CD%

set MCG_CONFIG_BIN_VERSION=1.3.0.2
set USERNAME=tburri
set GBE_PASSW=

set REMOTE_VERSION=
set LOCAL_VERSION=
set CLEANUP=0
set COPY_TEST=0
set COPY_TEST_ONLY=0
set BUILD=0

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
) else if "%~1"=="-c" (
	set CLEANUP=1
) else if "%~1"=="-t" (
	set COPY_TEST=1
) else if "%~1"=="-to" (
	set COPY_TEST=1
	set COPY_TEST_ONLY=1
) else if "%~1"=="-b" (
	set BUILD=1
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

set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION%\04_cfg
set LOCAL_VERSION2=4.%LOCAL_VERSION:~2,15%
set LOCAL_PATH2=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION2%\04_cfg
set LOCAL_VERSION4=5.%LOCAL_VERSION:~2,15%
set LOCAL_PATH4=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION4%\04_cfg

echo Version NRTOS2 %LOCAL_VERSION2%
echo Version NRTOS4 %LOCAL_VERSION4%

set REMOTE_BIN_PATH=%USERNAME%@files.scan.bombardier.com:/opt/repository/components/mcg_config_bin/%MCG_CONFIG_BIN_VERSION%/output
set REMOTE_PATH=%USERNAME%@files.scan.bombardier.com:/opt/repository/components/mcg_config/%REMOTE_VERSION%

if %COPY_TEST_ONLY% EQU 0 (
    echo Coyping now version MCG Config build %REMOTE_VERSION% from GBE repository to QNAP MCG Test Software Version %LOCAL_VERSION% / %LOCAL_VERSION2% ...

    REM copy first NRTOS 1 build
    if %CLEANUP% EQU 1 (
        echo ... first clean-up ...
        echo rmdir /S /Q %LOCAL_PATH%
        rmdir /S /Q %LOCAL_PATH% > nul
    )

    if not exist %LOCAL_PATH%\01_bin (
        mkdir %LOCAL_PATH%\01_bin
    )

    echo Copy mcg_config_bin
    echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_BIN_PATH%/* %LOCAL_PATH%\01_bin
    %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_BIN_PATH%/* %LOCAL_PATH%\01_bin


    echo Copy mcg_config
    echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg/* %LOCAL_PATH%
    %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg/* %LOCAL_PATH%
    echo.

    REM copy NRTOS 2 build - after manipulating LOCAL_VERSION
    if %CLEANUP% EQU 1 (
        echo ... first clean-up ...
        echo rmdir /S /Q %LOCAL_PATH%
        rmdir /S /Q %LOCAL_PATH% > nul
    )

    if not exist %LOCAL_PATH%\01_bin (
        mkdir %LOCAL_PATH%\01_bin
    )

    echo Copy mcg_config_bin
    echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_BIN_PATH%/* %LOCAL_PATH%\01_bin
    %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_BIN_PATH%/* %LOCAL_PATH%\01_bin


    echo Copy mcg_config
    echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg2/* %LOCAL_PATH%
    %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/mcg2/* %LOCAL_PATH%
    echo.

    if %COPY_TEST% EQU 1 (
        echo Copying test scripts from Test SVN
        echo .. first clean-up
        echo rmdir /S /Q %LOCAL_PATH%\20_tests
        rmdir /S /Q %LOCAL_PATH%\20_tests > nul

        echo svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH%\20_tests
        svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH%\20_tests
        echo.
    )


    REM copy NRTOS 4 build - after manipulating LOCAL_VERSION
    set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION4%\04_cfg
    if %CLEANUP% EQU 1 (
        echo ... first clean-up ...
        echo rmdir /S /Q %LOCAL_PATH%
        rmdir /S /Q %LOCAL_PATH% > nul
    )

    if not exist %LOCAL_PATH%\01_bin (
        mkdir %LOCAL_PATH%\01_bin
    )

    echo Copy mcg_config_bin
    echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_BIN_PATH%/* %LOCAL_PATH%\01_bin
    %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_BIN_PATH%/* %LOCAL_PATH%\01_bin


    echo Copy mcg_config
    echo %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/nrtos4/* %LOCAL_PATH%
    %PSCP_BIN% -r -pw %GBE_PASSW% %REMOTE_PATH%/dlu/nrtos4/* %LOCAL_PATH%
    echo.
)


if %COPY_TEST% EQU 1 (
    echo Copying test scripts from Test SVN
    echo .. first clean-up
    rmdir /S /Q %LOCAL_PATH%\20_tests > nul
    rmdir /S /Q %LOCAL_PATH2%\20_tests > nul
    rmdir /S /Q %LOCAL_PATH4%\20_tests > nul

    echo svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH%\20_tests
    svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH%\20_tests
    echo.

    echo svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH2%\20_tests
    svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH2%\20_tests

    echo svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH4%\20_tests
    svn export svn://qnap.tcms.ch/share/MD0_DATA/svn/mcg-test/trunk/TestEnvironment/00_TCMS_Software/01_MCG/01_Configurations/20_tests_release_config %LOCAL_PATH4%\20_tests
    echo.
)

if %BUILD% EQU 1 (
    if exists %LOCAL_PATH%\20_tests (
        %LOCAL_PATH%\20_tests\Execute_TestCases.cmd -buildonly -v %LOCAL_VERSION%.0
    ) else (
        %LOCAL_PATH%\build.all %LOCAL_VERSION%.0
    )

    if exists %LOCAL_PATH2%\20_tests (
        %LOCAL_PATH2%\20_tests\Execute_TestCases.cmd -buildonly -v %LOCAL_VERSION2%.0
    ) else (
        %LOCAL_PATH2%\build.all %LOCAL_VERSION2%.0
    )

    if exists %LOCAL_PATH4%\20_tests (
        %LOCAL_PATH4%\20_tests\Execute_TestCases.cmd -buildonly -v %LOCAL_VERSION4%.0
    ) else (
        %LOCAL_PATH4%\build.all %LOCAL_VERSION4%.0
    )
)


goto end

:error
echo Wrong or missing parameter
echo Usage:
echo Copy MCG Config from remote (source) to QNAP MCG Test Sofware (destination)
echo %FILENAME% [-s V.R.U.E] [-d V.R.U[.E]] [-c]
echo    -s V.R.U.E      source version from GBE repository
echo    -d V.R.U[.E]    destionation version / directory on QNAP
echo    -u              GBE Username
echo    -p              Password
echo    -c              clean-up before copying
echo    -t              copy test MDLs from Test SVN (default: off)
echo    -to             only copy test MDLs from Test SVN
echo    -b              build dlus (if tests exists, build with this)
echo.

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
