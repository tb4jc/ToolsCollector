@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
set FILENAME=%~n0%~x0

REM Batch file to create config tags for MCG Platform Releases
REM Param 1 - branch name e.g. 3.21.0.x
REM Param 2 - r.u.e

echo.
echo ===== Creating config tags for MCG Platform Release =====
echo.

set REL_BRANCH_VERSION=
set TAG_VERSION=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-b" (
	if "%~2"=="" goto error
	set REL_BRANCH_VERSION=%~2
	shift
) else if "%~1"=="-t" (
	if "%~2"=="" goto error
	set TAG_VERSION=%~2
	shift
) else (
	goto error
)
shift
goto parse

:endparse

if "%REL_BRANCH_VERSION%"=="" (
	set /p REL_BRANCH_VERSION="Enter version of MCG Config Release Branch (V.R.U.x or name): "
)

if "%TAG_VERSION%"=="" (
	set /p TAG_VERSION="Enter version of MCG Config Release Tag (3.R.U.E): "
)

:create
echo Release branch: %REL_BRANCH_VERSION%
echo Tag Versions:   %TAG_VERSION%

svn proplist http://10.160.151.2:3690/svn/components/mcg/generic/mcg_config/tags/%TAG_VERSION% > NUL
if not errorlevel 1 goto exists

echo Calling 'svn cp http://10.160.151.2:3690/svn/components/mcg/generic/mcg_config/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/components/mcg/generic/mcg_config/tags/%TAG_VERSION% -m "MCG Platform Release %TAG_VERSION%"'
svn cp http://10.160.151.2:3690/svn/components/mcg/generic/mcg_config/branches/%REL_BRANCH_VERSION% http://10.160.151.2:3690/svn/components/mcg/generic/mcg_config/tags/%TAG_VERSION% -m "MCG Platform Release %TAG_VERSION%"
if errorlevel 1 (
    echo Creating SVN MCG Config tag %TAG_VERSION% failed
    goto EOF
)

echo done
goto EOF


:exists
echo Tag %TAG_VERSION% already exists!
goto EOF


:error
echo Wrong or missing parameter
echo Usage:  %FILENAME% [-b V.R.U.E] [-t V.R.U.E]
echo.
echo V is always the base version (3), 4 and 5 are build automatically

:EOF
echo.
pause
