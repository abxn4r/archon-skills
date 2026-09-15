@echo off
rem Archon Windows CLI executable launcher
rem 100% zero-dependency Standard Library implementation

setlocal EnableDelayedExpansion

set "ARCHON_BIN_DIR=%~dp0"
pushd "%ARCHON_BIN_DIR%.."
set "ARCHON_ROOT=%CD%"
popd

set "PYTHON_EXE="
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PYTHON_EXE=python"
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=py -3"
    ) else (
        where python3 >nul 2>nul
        if %ERRORLEVEL% equ 0 (
            set "PYTHON_EXE=python3"
        )
    )
)

if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python 3 is required to run Archon but was not found on PATH. >&2
    exit /b 1
)

if defined PYTHONPATH (
    set "PYTHONPATH=%ARCHON_ROOT%;%PYTHONPATH%"
) else (
    set "PYTHONPATH=%ARCHON_ROOT%"
)

%PYTHON_EXE% -m archon.cli %*
exit /b %ERRORLEVEL%
