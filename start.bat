@echo off
setlocal


set CURRENT_DIRECTORY=%~dp0
set ENV_NAME=env
set VENV=%CURRENT_DIRECTORY%\%ENV_NAME%\Scripts

cd %CURRENT_DIRECTORY%

python -m venv %ENV_NAME%
call %VENV%\activate

%VENV%\python -m pip install --upgrade pip
%VENV%\python -m pip install -r %PROJECT%\requirements.txt
%VENV%\python %PROJECT%\src\main.py
