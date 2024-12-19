@echo off
if exist .venv\ (
  echo Virtual environment already exists, skipping
  echo Activating virtual environment
  .venv\Scripts\activate.bat
  pip install -r requirements.txt
  if "%~1" == "" (
  py main.py
  ) else (
  py main.py -c "%~1"
  )
) else (
  echo Creating virtual environment...
  py -3.12 -m venv .venv
  echo Activating virtual environment
  .venv\Scripts\activate.bat
  echo Installing required packages
  pip install -r requirements.txt
  if "%~1" == "" (
  py main.py
  ) else (
  py main.py -c "%~1"
  )
)
