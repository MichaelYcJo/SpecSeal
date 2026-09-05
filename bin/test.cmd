@echo off
rem Windows counterpart to bin/test, kept in lockstep with it: a bin/ entry is
rem a pair, or it is one platform. Note that POSIX shells resolve a bare
rem `test` to their own builtin, so both files are typed as bin/test.
setlocal
set "here=%~dp0"
set "script=%here%..\.github\scripts\run_tests.py"

if not exist "%script%" (
  echo bin/test runs SpecSeal's own test suite, and this copy of bin/ has no runner beside it. Run it from a clone of the SpecSeal repository. 1>&2
  exit /b 2
)

where /q py
if errorlevel 1 goto usepython
py -3 "%script%" %*
exit /b %errorlevel%

:usepython
python "%script%" %*
exit /b %errorlevel%
