@echo off
rem Windows counterpart to bin/seal: cmd.exe/PowerShell resolve a bare `seal`
rem to this file via PATHEXT, the same way POSIX shells resolve the
rem extensionless sibling. Kept in lockstep with it.
setlocal
set "here=%~dp0"
set "script=%here%..\skills\implement\scripts\seal.py"

where /q py
if errorlevel 1 goto usepython
py -3 "%script%" %*
exit /b %errorlevel%

:usepython
python "%script%" %*
exit /b %errorlevel%
