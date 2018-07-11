@echo off
echo "Copying build from GBE_ch (drive v:) to local NAS installation"
set CWD=%CD%

set LOCAL_VERSION=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-d" (
	if "%~2"=="" goto error
	set LOCAL_VERSION=%~2
	shift
) else (
	goto error
)
shift
goto parse
:endparse

if "%LOCAL_VERSION%"=="" (
	set /p LOCAL_VERSION="Enter version on NAS installation: "
)

set LOCAL_VERSION2=4.%LOCAL_VERSION:~2,15%
set LOCAL_VERSION4=5.%LOCAL_VERSION:~2,15%
echo %LOCAL_VERSION2%
echo %LOCAL_VERSION4%

echo "Coyping now version MCG Firmware build 'v:\mcgfirmware-trunk-tb' from GBE_ch drive to NAS Installation Version %LOCAL_VERSION% / %LOCAL_VERSION2% / %LOCAL_VERSION4% ..."

set REMOTE_PATH=v:\mcgfirmware-trunk-tb\component
set LOCAL_PATH=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION%
cd ..

REM copy first NRTOS 1 build
echo "xcopy %REMOTE_PATH%\dlu\mcg\*  %LOCAL_PATH%\03_mcg_firmware /E /F /Y"
xcopy %REMOTE_PATH%\dlu\mcg\*  %LOCAL_PATH%\03_mcg_firmware /E /F /Y
echo "xcopy %REMOTE_PATH%\dlu\mcg\3rd_party\*  %LOCAL_PATH%\06_3rd_party /E /F /Y"
xcopy %REMOTE_PATH%\dlu\mcg\3rd_party\*  %LOCAL_PATH%\06_3rd_party /E /F /Y

REM copy NRTOS 2 build - after manipulating LOCAL_VERSION
set LOCAL_PATH2=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION2%
echo "xcopy %REMOTE_PATH%\dlu\mcg2\*  %LOCAL_PATH2%\03_mcg_firmware /E /F /Y"
xcopy %REMOTE_PATH%\dlu\mcg2\*  %LOCAL_PATH2%\03_mcg_firmware /E /F /Y
echo "xcopy %REMOTE_PATH%\dlu\mcg2\3rd_party\*  %LOCAL_PATH2%\06_3rd_party /E /F /Y"
xcopy %REMOTE_PATH%\dlu\mcg2\3rd_party\*  %LOCAL_PATH2%\06_3rd_party /E /F /Y

REM copy NRTOS 4 build - after manipulating LOCAL_VERSION
set LOCAL_PATH4=\\hermes40\public\06_Integration_Test_Enviroment\00_TCMS_Software\01_MCG\%LOCAL_VERSION4%
echo "xcopy %REMOTE_PATH%\dlu\nrtos4\*  %LOCAL_PATH4%\03_mcg_firmware /E /F /Y"
xcopy %REMOTE_PATH%\dlu\nrtos4\*  %LOCAL_PATH4%\03_mcg_firmware /E /F /Y

goto end

:error
echo "Wrong or missing parameter"
echo "Usage:"
echo "copy-build-from-v-to-install-loc.cmd [-s V.R.U.E] [-d V.R.U.E]"
echo
echo "Copy MCG Firmware from remote (source) to local (destination)"

:end

echo "... done"
cd %CWD%
