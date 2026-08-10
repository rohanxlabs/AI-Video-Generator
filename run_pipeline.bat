@echo off
REM Batch script to run the AI Video Generator pipeline in the virtual environment

echo ======================================================================
echo AI VIDEO GENERATOR - Pipeline Runner
echo ======================================================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python setup.py
    pause
    exit /b 1
)

REM Activate virtual environment and run pipeline
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running pipeline with your prompt...
echo.

REM Pass all arguments to the pipeline script
python pipeline.py %*

echo.
echo ======================================================================
pause
