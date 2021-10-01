@echo off
echo Cinema plugin add
echo -----------------

set /p Input=Input path to Prism root: 
cd %~dp0
rmdir %Input%"\Plugins\Apps\Cinema"
mkdir %Input%"\Plugins\Apps\Cinema"
del %Input%"\ProjectFiles\EmptyScenes\EmptyScene Cinema R23.c4d"

xcopy ".\Integration" %Input%"\Plugins\Apps\Cinema\Integration" /s /e /y /i /o
xcopy ".\Scripts" %Input%"\Plugins\Apps\Cinema\Scripts" /s /e /y /i /o
xcopy /S /Q /Y /F ".\Integration\EmptyScene Cinema R23.c4d" %Input%"\ProjectFiles\EmptyScenes\"


echo Complite
pause