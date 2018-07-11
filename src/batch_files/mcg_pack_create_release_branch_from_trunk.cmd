@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
set FILENAME=%~n0%~x0

REM Batch file to create pack release branch for MCG Platform Release Installers
REM Param 1 - release branch name e.g. 3.21.0.x

echo.
echo ===== Creating release branch for MCG Platform Release =====
echo.

set REL_BRANCH_VERSION=

:parse
if "%~1"=="" goto endparse
if "%~1"=="-b" (
	if "%~2"=="" goto error
	set REL_BRANCH_VERSION=%~2
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

:create
echo Create Release branch: %REL_BRANCH_VERSION%

svn proplist http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% > NUL
if not errorlevel 1 goto exists

echo Calling 'svn cp http://10.160.151.2:3690/svn/package/mcg/trunk http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% -m "MCG Platform Release branche %REL_BRANCH_VERSION%"'
svn cp http://10.160.151.2:3690/svn/package/mcg/trunk http://10.160.151.2:3690/svn/package/mcg/branches/%REL_BRANCH_VERSION% -m "MCG Platform Release branche %REL_BRANCH_VERSION%"
if errorlevel 1 (
    echo Creating SVN MCG Pack tag %NRTOS1_TAG_VERSION% failed
    goto EOF
)

echo done
goto EOF

:exists
echo Release branch %REL_BRANCH_VERSION% already exists!
goto EOF


:error
echo Wrong or missing parameter
echo Usage:  %FILENAME% [-b V.R.U.E]
echo.
echo V shall always be the base version (3)


:EOF
echo.
pause
