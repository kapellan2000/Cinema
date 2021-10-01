@echo off
echo Cinema plugin add
echo -----------------
set /p Input=Input path to Prism root: 
DirName=%cd% 
cd %DirName%
dir
rmdir %Input%"\Plugins\Apps\Cinema"
mkdir %Input%"\Plugins\Apps\Cinema"

xcopy %DirName%"\Integration" %Input%"\Plugins\Apps\Cinema\Integration" /s /e /y /i /o
xcopy %DirName%"\Scripts" %Input%"\Plugins\Apps\Cinema\Scripts" /s /e /y /i /o

echo Complite
pause