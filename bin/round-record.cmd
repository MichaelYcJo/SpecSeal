@echo off
rem Windows counterpart to bin/round-record: cmd.exe/PowerShell resolve a
rem bare `round-record` to this file via PATHEXT, the same way POSIX
rem shells resolve the extensionless sibling. Kept in lockstep with it.
setlocal
set "here=%~dp0"
set "script=%here%..\skills\code-review\scripts\round_record.py"

where /q py
if errorlevel 1 goto usepython
py -3 "%script%" %*
exit /b %errorlevel%

:usepython
python "%script%" %*
exit /b %errorlevel%
