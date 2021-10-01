@echo off
echo Cinema plugin add
echo -----------------

set /p Input=Input path to Prism root: 
cd %~dp0
dir
pause
rmdir %Input%"\Plugins\Apps\Cinema"
mkdir %Input%"\Plugins\Apps\Cinema"

xcopy ".\Integration" %Input%"\Plugins\Apps\Cinema\Integration" /s /e /y /i /o
xcopy ".\Scripts" %Input%"\Plugins\Apps\Cinema\Scripts" /s /e /y /i /o
xcopy ".\Integration\EmptyScene Cinema R23.c4d" %Input%"\ProjectFiles\EmptyScenes" /s /e /y /i /o
echo Complite
pause