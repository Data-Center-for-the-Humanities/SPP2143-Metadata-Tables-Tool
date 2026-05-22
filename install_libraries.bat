@echo off
setlocal ENABLEDELAYEDEXPANSION

echo =====================================
echo Checking Python installation...
echo =====================================

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
    ) else (
        echo Python was not found on this system.
        pause
        exit /b 1
    )
)

echo Using %PYTHON_CMD%
echo.

echo =====================================
echo Checking required modules...
echo =====================================

REM Liste der zu pruefenden Module mit Paketzuordnung (modul|paket)
set "MODULE_MAP=requests|requests pandas|pandas openpyxl|openpyxl PIL|Pillow geopandas|geopandas shapely|shapely"

for %%P in (%MODULE_MAP%) do (
    for /f "tokens=1,2 delims=|" %%A in ("%%P") do (
        echo Checking %%A ...
        %PYTHON_CMD% -c "import %%A" 2>nul
    if errorlevel 1 (
            echo Module %%A not found. Installing package %%B...
            %PYTHON_CMD% -m pip install %%B
    ) else (
            echo Module %%A is already installed.
        )
        echo.
    )
)

echo =====================================
echo Checking tkinter availability...
echo =====================================

%PYTHON_CMD% -c "import tkinter" 2>nul
if errorlevel 1 (
    echo WARNING: tkinter is not available in this Python installation.
    echo You may need to reinstall Python and enable Tcl/Tk support.
) else (
    echo tkinter is available.
)

echo.
echo Done.
pause