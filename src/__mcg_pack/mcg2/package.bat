@echo off
:: batch-create SCI and Device Package
:: GB_COMP_REPOSITORY = repository of the components
:: GB_BUILDTOOLS_REPOSITORY = reporitory of the build tools
:: GB_DELIVERY_ROOT = where delivery should be placed
:: GB_PACK_ROOT = location of the pack folder from where to get the *.inc files
:: GB_LOG_ROOT = path to log directory
:: VERSION = Version of the product

:: remove for local test ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
REM set GB_COMP_REPOSITORY=R:\components
REM set GB_BUILDTOOLS_REPOSITORY=R:\buildtools
REM set GB_PACK_ROOT=c:\workspace\TCMS\MCG-Pack
REM set GB_DELIVERY_ROOT=%GB_PACK_ROOT%\Products\%TARGET_NAME%\%VERSION%\delivery_dp
REM set GB_LOG_ROOT=%GB_PACK_ROOT%\logs_dp
REM set VERSION=3.17.0.0
REM mkdir %GB_LOG_ROOT%
REM mkdir %GB_DELIVERY_ROOT%


:: Need to be setup by the developer
set WORKSPACE=%GB_PACK_ROOT%\workspace
set MTPKG_PATH=%GB_BUILDTOOLS_REPOSITORY%\mtpkg\1.4.0.93
set MTPKG_EXE=%MTPKG_PATH%\MTPKG.exe
set MAKEDLU_PATH=%GB_BUILDTOOLS_REPOSITORY%\makedlu\win32\2.7.0.2\makedlu.exe
set GBEGETVERSION_PATH=%GB_BUILDTOOLS_REPOSITORY%\GBEGetVersion\1.0.1.0\GBEGetVersion.exe

set VERSIONS_INC=%GB_PACK_ROOT%\versions.inc
set PACKAGE_INC=%GB_PACK_ROOT%\devpack\device_pack.inc

echo "environment variables are set now"
echo "reading in device_pack.inc ..."

:: Get from device_pack_info.inc file !*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% TARGET_NAME %PACKAGE_INC%') Do Set TARGET_NAME=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% DEVTYPE %PACKAGE_INC%') Do Set DEVTYPE=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% DEVTARGET %PACKAGE_INC%') Do Set DEVTARGET=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCIDEVTYPE %PACKAGE_INC%') Do Set SCIDEVTYPE=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SOURCE %PACKAGE_INC%') Do Set SOURCE=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% RESERVED %PACKAGE_INC%') Do Set RESERVED=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% FUNCTION %PACKAGE_INC%') Do Set FUNCTION=%%i
set RESERVEDFUNCTION=%RESERVED%-%FUNCTION%

if "%TARGET_NAME%"=="mcg" (
	set TARGET_NAME_FALLBACK=ccuc
) else (
	set TARGET_NAME_FALLBACK=nrtos
)

:: Path of temporary MTPKG Repository
set REPOSITORY=%WORKSPACE%\00-Rep-%RESERVEDFUNCTION%
mkdir %REPOSITORY%

%MTPKG_EXE% SetRepository %REPOSITORY%
if not %errorlevel%==0 (
	echo [Error] SetRepository %REPOSITORY% failed
	goto exit_with_error
)

%MTPKG_EXE% AddPF %SCIDEVTYPE%
if not %errorlevel%==0 (
	echo [Error] AddPF %SCIDEVTYPE% failed
	goto exit_with_error
)

echo "creating sci one - mcg stand ..."

:: Create the SCI1  ==========================================================================
:: Get from device_pack_info.inc file !*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCI1SUBFCT %PACKAGE_INC%') Do Set SCI1SUBFCT=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCI1VERSION %PACKAGE_INC%') Do Set SCI1VERSION=%%i

:: Get from versions.inc file -----------------------------------------------------------------
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% mcg_firmware %VERSIONS_INC%') Do Set MCGFIRMWAREVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% mcg_config %VERSIONS_INC%') Do Set MCGCONFIGVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% tds-com %VERSIONS_INC%') Do Set TDSCOMVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% tds-tcl %VERSIONS_INC%') Do Set TDSTCLVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% tssp-ip %VERSIONS_INC%') Do Set TSSPIPVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% vrs-ip %VERSIONS_INC%') Do Set VRSIPVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% qt-build %VERSIONS_INC%') Do Set QTBUILDVERSION=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% cm %VERSIONS_INC%') Do Set CMVERSION=%%i

echo "... creating mcg stand sci master dlu ..."

REM splitting TDSCOM, TDSTCL and VRS versions
SETLOCAL ENABLEDELAYEDEXPANSION
for /f "tokens=1-4 delims=." %%a in ("%VRSIPVERSION: by=.%") do (
	set VRSIPVERSION_FLAT=%%a%%b%%c%%d
)

:: Create SCI Master DLU for base package
%MAKEDLU_PATH% ^
%GB_COMP_REPOSITORY%\mcg_config\%MCGCONFIGVERSION%\dlu\%TARGET_NAME%\06_mcg_firmware_cfg\mcg_master_cfg\for_remote_download\%RESERVEDFUNCTION%_%SCI1SUBFCT%_%DEVTYPE%_%SOURCE%.xml ^
%RESERVEDFUNCTION%_%SCI1SUBFCT%_%DEVTYPE%_%SOURCE% ^
%SCI1VERSION% ^
0x00000042 ^
OUTFILE %WORKSPACE%\%RESERVEDFUNCTION%_%SCI1SUBFCT%_%DEVTYPE%_%SOURCE%.dl2

echo "... calling mtpkg tool ..."

%MTPKG_EXE% --force createsci %RESERVEDFUNCTION% %SCI1SUBFCT% %SCIDEVTYPE% %SCI1VERSION% %SOURCE% ^
%WORKSPACE%\%RESERVEDFUNCTION%_%SCI1SUBFCT%_%DEVTYPE%_%SOURCE%.dl2 ^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_base1_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_base2_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_framewrk1_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_framewrk2_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_gfus_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_services_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_traininfo_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_tsspsrv_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_tsspsrvng_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_wakeuptrn_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_tdsmsg_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\tds-com\%TDSCOMVERSION%\dlu\%TARGET_NAME_FALLBACK%\0000-tds_com_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\tds-tcl\%TDSTCLVERSION%\dlu\%TARGET_NAME_FALLBACK%\0000-tds_tcl_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\tssp-ip\%TSSPIPVERSION%\dlu\%TARGET_NAME%\dlu_new\0000-tssp_client_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\vrs-ip\%VRSIPVERSION%\dlu\%TARGET_NAME%\vrsReportDvsHw_%VRSIPVERSION_FLAT%.dl2,^
%GB_COMP_REPOSITORY%\vrs-ip\%VRSIPVERSION%\dlu\%TARGET_NAME%\vrsReportDvsHw2_%VRSIPVERSION_FLAT%.dl2,^
%GB_COMP_REPOSITORY%\vrs-ip\%VRSIPVERSION%\dlu\%TARGET_NAME%\vrsClient_%VRSIPVERSION_FLAT%.dl2,^
%GB_COMP_REPOSITORY%\vrs-ip\%VRSIPVERSION%\dlu\%TARGET_NAME%\vrsReportDvsSw_%VRSIPVERSION_FLAT%.dl2,^
%GB_COMP_REPOSITORY%\vrs-ip\%VRSIPVERSION%\dlu\%TARGET_NAME%\vrsReportDvsSw2_%VRSIPVERSION_FLAT%.dl2,^
%GB_COMP_REPOSITORY%\vrs-ip\%VRSIPVERSION%\dlu\%TARGET_NAME%\vrsServer_%VRSIPVERSION_FLAT%.dl2,^
%GB_COMP_REPOSITORY%\qt-build\%QTBUILDVERSION%\dlu\%TARGET_NAME_FALLBACK%\0000-qt_%DEVTYPE%.dl2,^
%GB_COMP_REPOSITORY%\cm\%CMVERSION%\dlu\%TARGET_NAME%\0000-cm_%DEVTYPE%.dl2 ^
false ^
SaveLog %GB_LOG_ROOT%\create%SCI1SUBFCT%.log
if not %errorlevel%==0 (
	echo [Error] create%SCI1SUBFCT% failed
	goto exit_with_error
)

echo "creating sci two - mcg gsmdump ..."

:: Create the SCI2  ============================================================================
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCI2SUBFCT %PACKAGE_INC%') Do Set SCI2SUBFCT=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCI2VERSION %PACKAGE_INC%') Do Set SCI2VERSION=%%i

echo "... creating sci master for GSM Dump ..."

:: Create SCI Master DLU for GSM Dump package
%MAKEDLU_PATH% ^
%GB_COMP_REPOSITORY%\mcg_config\%MCGCONFIGVERSION%\dlu\%TARGET_NAME%\06_mcg_firmware_cfg\mcg_master_cfg\for_remote_download\%RESERVEDFUNCTION%_gsmdump_%DEVTYPE%_%SOURCE%.xml ^
%RESERVEDFUNCTION%_gsmdump_%DEVTYPE%_%SOURCE% ^
%SCI2VERSION% ^
0x00000042 ^
OUTFILE %WORKSPACE%\%RESERVEDFUNCTION%_gsmdump_%DEVTYPE%_%SOURCE%.dl2

echo "... calling mtpkg ..."

%MTPKG_EXE% --force createsci %RESERVEDFUNCTION% %SCI2SUBFCT% %SCIDEVTYPE% %SCI2VERSION% %SOURCE% ^
%WORKSPACE%\%RESERVEDFUNCTION%_gsmdump_%DEVTYPE%_%SOURCE%.dl2 ^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_gsmdump_%DEVTYPE%.dl2 ^
false ^
SaveLog %GB_LOG_ROOT%\create%SCI2SUBFCT%.log
if not %errorlevel%==0 (
	echo [Error] create%SCI2SUBFCT% failed
	goto exit_with_error
)


echo "creating sci three - mcg videostrm ..."

:: Create the SCI3  ============================================================================
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCI3SUBFCT %PACKAGE_INC%') Do Set SCI3SUBFCT=%%i
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% SCI3VERSION %PACKAGE_INC%') Do Set SCI3VERSION=%%i

echo "... creating sci master for mcg videostrm ..."

:: Create SCI Master DLU for videostrm package
%MAKEDLU_PATH% ^
%GB_COMP_REPOSITORY%\mcg_config\%MCGCONFIGVERSION%\dlu\%TARGET_NAME%\06_mcg_firmware_cfg\mcg_master_cfg\for_remote_download\%RESERVEDFUNCTION%_%SCI3SUBFCT%_%DEVTYPE%_%SOURCE%.xml ^
%RESERVEDFUNCTION%_%SCI3SUBFCT%_%DEVTYPE%_%SOURCE% ^
%SCI3VERSION% ^
0x00000042 ^
OUTFILE %WORKSPACE%\%RESERVEDFUNCTION%_%SCI3SUBFCT%_%DEVTYPE%_%SOURCE%.dl2

echo "... calling mtpkg for mcg videostrm ..."

%MTPKG_EXE% --force createsci %RESERVEDFUNCTION% %SCI3SUBFCT% %SCIDEVTYPE% %SCI3VERSION% %SOURCE% ^
%WORKSPACE%\%RESERVEDFUNCTION%_%SCI3SUBFCT%_%DEVTYPE%_%SOURCE%.dl2 ^
%GB_COMP_REPOSITORY%\mcg_firmware\%MCGFIRMWAREVERSION%\dlu\%TARGET_NAME%\%RESERVEDFUNCTION%_%SCI3SUBFCT%_%DEVTYPE%.dl2 ^
false ^
SaveLog %GB_LOG_ROOT%\create%SCI3SUBFCT%.log
if not %errorlevel%==0 (
	echo [Error] create%SCI3SUBFCT% failed
	goto exit_with_error
)


echo "creating devivce package (FP)..."

rem create the Device Package ==========================================================================
%MTPKG_EXE% --force createFP %VERSION% %SOURCE% 1 ^
%REPOSITORY%\SCI\%RESERVEDFUNCTION%_%SCI1SUBFCT%\%SCIDEVTYPE%\%SCI1VERSION%\%RESERVEDFUNCTION%_%SCI1SUBFCT%_%SCIDEVTYPE%_%SOURCE%.sci,^
%REPOSITORY%\SCI\%RESERVEDFUNCTION%_%SCI2SUBFCT%\%SCIDEVTYPE%\%SCI2VERSION%\%RESERVEDFUNCTION%_%SCI2SUBFCT%_%SCIDEVTYPE%_%SOURCE%.sci,^
%REPOSITORY%\SCI\%RESERVEDFUNCTION%_%SCI3SUBFCT%\%SCIDEVTYPE%\%SCI3VERSION%\%RESERVEDFUNCTION%_%SCI3SUBFCT%_%SCIDEVTYPE%_%SOURCE%.sci ^
SaveLog %GB_LOG_ROOT%\logFP.txt
if not %errorlevel%==0 (
	echo [Error] CreateEDSP failed
	goto exit_with_error
)


echo "copying FP ..."
set DEVPACKRESULT=%GB_DELIVERY_ROOT%\09_dev_pack
mkdir %DEVPACKRESULT%
rem copy the Device Package from the temporary MTPKG Repository to the TCMS Repository
copy %REPOSITORY%\FP\%RESERVEDFUNCTION%\%VERSION%\*.fp %DEVPACKRESULT%\*
if not %errorlevel%==0 (
	echo [Error] Failed copying DP to delivery_dp
	goto exit_with_error
)


:osbase
echo "copying OS Base parts ..."

rem copy 01 os_base content
set OsBaseRESULT=%GB_DELIVERY_ROOT%\01_os_base
mkdir %OsBaseRESULT%
set OSComponent=nrtos_prod_base
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% %OSComponent% %VERSIONS_INC%') Do Set rtsversion=%%i
copy /Y %GB_COMP_REPOSITORY%\%OSComponent%\%rtsversion%\dlu\%TARGET_NAME%\0000-rts_%DEVTYPE%.dl2 %OsBaseRESULT%\*
if not %errorlevel%==0 (
	echo [Error] Failed copying 01_os_base
	goto exit_with_error
)

echo "copying 04_config ..."

rem copy 04_config content
set ConfigRESULT=%GB_DELIVERY_ROOT%\04_cfg
mkdir %ConfigRESULT%
set mcgconfigComponent=mcg_config
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% %mcgconfigComponent% %VERSIONS_INC%') Do Set mcgconfversion=%%i
xcopy /Y %GB_COMP_REPOSITORY%\%mcgconfigComponent%\%mcgconfversion%\dlu\%TARGET_NAME%\* %ConfigRESULT%\* /s
if not %errorlevel%==0 (
	echo [Error] Failed copying 04_cfg
	goto exit_with_error
)

echo "copying 04_config bin ..."

rem copy 04_config_bin content
set ConfigBinRESULT=%GB_DELIVERY_ROOT%\04_cfg\01_bin
mkdir %ConfigBinRESULT%
set mcgconfigBinComponent=mcg_config_bin
For /F "tokens=* delims=" %%i in ('%GBEGETVERSION_PATH% %mcgconfigBinComponent% %VERSIONS_INC%') Do Set mcgconfBinversion=%%i
copy /Y %GB_COMP_REPOSITORY%\%mcgconfigBinComponent%\%mcgconfBinversion%\output\* %ConfigBinRESULT%\*
if not %errorlevel%==0 (
	echo [Error] Failed copying 04_cfg\01_bin
	goto exit_with_error
)

echo "copying mtpkg tool ..."
set ConfigBinRESULT=%GB_DELIVERY_ROOT%\04_cfg\01_bin\mtpkg
mkdir %ConfigBinRESULT%
xcopy /Y %MTPKG_PATH%\* %ConfigBinRESULT%\* /s
if not %errorlevel%==0 (
	echo [Error] Failed copying mtpkg to 04_cfg\01_bin\mtpkg
	goto exit_with_error
)


echo "finished, cleaning up temporary dirs"

:exit
:: Remove tempory repository
rmdir %REPOSITORY% /S /Q
exit /b 0

:exit_with_error
:: Remove tempory repository
rmdir %REPOSITORY% /S /Q
exit /b 1