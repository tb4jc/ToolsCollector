@echo off

echo start
set QNAP_DRIVE_LETTER=y

if "%QNAP_DRIVE_LETTER%"=="" (
    echo Drive letter of QNAP attaching not given - calling configuration build script skipped
) else (
    echo Executing configuration builder
)

echo done

