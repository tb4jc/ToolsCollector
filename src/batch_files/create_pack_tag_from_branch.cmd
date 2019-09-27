@echo off
setlocal enabledelayedexpansion

if exist ..\..\ansi.txt echo [1;33m
echo ==============================================
echo  Create pack tags from branch
echo ==============================================
if exist ..\..\ansi.txt echo [1;32m

REM Batch file to create pack tags for MCG Platform Releases
REM option '-b' - branch name e.g. 3.21.0.x
REM option '-t' - tag name for NRTOS1 based 3.r.u.e

set REL_BRANCH_VERSION=
set NRTOS1_TAG_VERSION=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-b" (
	if "%~2"=="" goto error
	set REL_BRANCH_VERSION=%~2
	shift
) else if "%~1"=="-t" (
	if "%~2"=="" goto error
	set NRTOS1_TAG_VERSION=%~2
	shift
) else (
	goto error
)
shift
goto parse

:endparse

if "%REL_BRANCH_VERSION%"=="" (
	set /p REL_BRANCH_VERSION="Enter version of MCG Pack Release Branch (V.R.U.x): "
)

if "%NRTOS1_TAG_VERSION%"=="" (
	set /p NRTOS1_TAG_VERSION="Enter version of MCG Pack Release Tag (only base 3, V.R.U.E): "
)

set NRTOS2_TAG_VERSION=4.%NRTOS1_TAG_VERSION:~2%
set NRTOS4_TAG_VERSION=5.%NRTOS1_TAG_VERSION:~2%


:create
echo Release branch: %REL_BRANCH_VERSION%
echo Tag Versions:   %NRTOS1_TAG_VERSION%, %NRTOS2_TAG_VERSION%, %NRTOS4_TAG_VERSION%

echo Calling "svn proplist http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS1_TAG_VERSION% > NUL"
svn proplist http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS1_TAG_VERSION% > NUL
if not errorlevel 1 goto exists1

echo Calling 'svn cp http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS1_TAG_VERSION% -m "MCG Platform Release %NRTOS1_TAG_VERSION%"'
svn cp http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS1_TAG_VERSION% -m "MCG Platform Release %NRTOS1_TAG_VERSION%"
if errorlevel 1 (
   echo Creating SVN MCG Pack tag %NRTOS1_TAG_VERSION% failed
   goto EOF
)
goto create2

:exists1
echo Release Tag %NRTOS1_TAG_VERSION% already exists!

:create2
echo Calling "svn proplist http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS2_TAG_VERSION% > NUL"
svn proplist http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS2_TAG_VERSION% > NUL
if not errorlevel 1 goto exists2

echo Calling 'svn cp http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS2_TAG_VERSION% -m "MCG Platform Release %NRTOS2_TAG_VERSION%"'
svn cp http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS2_TAG_VERSION% -m "MCG Platform Release %NRTOS2_TAG_VERSION%"
if not errorlevel 0 (
    echo Creating SVN MCG Pack tag %NRTOS2_TAG_VERSION% failed
    goto EOF
)
goto create4

:exists2
echo Release Tag %NRTOS2_TAG_VERSION% already exists!

:create4
echo Calling "svn proplist http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS4_TAG_VERSION% > NUL"
svn proplist http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS4_TAG_VERSION% > NUL
if not errorlevel 1 goto exists4

echo Calling 'svn cp http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS4_TAG_VERSION% -m "MCG Platform Release %NRTOS4_TAG_VERSION%"'
svn cp http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/package/mcg/tags/%NRTOS4_TAG_VERSION% -m "MCG Platform Release %NRTOS4_TAG_VERSION%"
if errorlevel 1 (
    echo Creating SVN MCG Pack tag %NRTOS4_TAG_VERSION% failed
    goto EOF
)

goto EOF

:exists4
echo Release Tag %NRTOS4_TAG_VERSION% already exists!
goto EOF

:error
echo Wrong or missing parameter
echo Usage:  %FILENAME% [-b V.R.U.E] [-t V.R.U.E]
echo.
echo V is always the base version (3), 4 and 5 are build automatically

:EOF
echo.
if exist ..\..\ansi.txt echo [1;33m
echo ==========================================
if exist ..\..\ansi.txt echo [0m

if "%REL_BRANCH_VERSION%"=="1.2.3.4" exit 1

REM EOF
