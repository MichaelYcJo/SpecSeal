@echo off
rem Windows counterpart to bin/mutation-check: cmd.exe/PowerShell resolve a bare
rem `mutation-check` to this file via PATHEXT, the same way POSIX shells resolve
rem the extensionless sibling. Kept in lockstep with it.
setlocal
set "here=%~dp0"
set "script=%here%..\skills\verify\scripts\mutation_check.py"

where /q py
if errorlevel 1 goto usepython
py -3 "%script%" %*
exit /b %errorlevel%

:usepython
python "%script%" %*
exit /b %errorlevel%
