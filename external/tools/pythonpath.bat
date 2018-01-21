@ECHO OFF
setlocal
set PYTHONPATH=%PYTHONPATH%;%1

set REST_VAR=
shift
:loop1
if "%1"=="" goto after_loop
set RESTVAR=%RESTVAR% %1
shift
goto loop1
:after_loop

REM @ECHO ON
REM echo cwd %cd%
REM echo python %RESTVAR%
REM @ECHO OFF
python %RESTVAR%
endlocal