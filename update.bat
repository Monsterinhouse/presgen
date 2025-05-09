@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
color 0a
cls

echo:
echo:
echo ██████╗  ██████╗  ███████╗ ███████╗  ██████╗  ███████╗ ███╗   ██╗
echo ██╔══██╗ ██╔══██╗ ██╔════╝ ██╔════╝ ██╔════╝  ██╔════╝ ████╗  ██║
echo ██████╔╝ ██████╔╝ █████╗   ███████╗ ██║  ███╗ █████╗   ██╔██╗ ██║
echo ██╔═══╝  ██╔══██╗ ██╔══╝   ╚════██║ ██║   ██║ ██╔══╝   ██║╚██╗██║
echo ██║      ██║  ██║ ███████╗ ███████║ ╚██████╔╝ ███████╗ ██║ ╚████║
echo ╚═╝      ╚═╝  ╚═╝ ╚══════╝ ╚══════╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝
echo:
echo:
echo Presione Enter para actualizar el programa
pause

python ./bin/update.py

:: Ejecuta pyinstaller en segundo plano
start "" /B cmd /c "pyinstaller .\bin\main.py --specpath .\specs\ --name Presgen --icon .\media\PressGenLogo.png --onedir -y" > pyinstaller_log.txt

:: Simular barra de progreso mientras pyinstaller corre
set "total=30"
set /a progress=0

:progress_loop
:: Verifica si pyinstaller sigue ejecutándose
tasklist | find /i "pyinstaller.exe" >nul
if %errorlevel%==0 (
    set /a progress+=1
    set "bar="
    
    for /L %%i in (1,1,!progress!) do set "bar=!bar!#"
    for /L %%i in (!progress!,1,%total%) do set "bar=!bar!."

    cls
    echo Generando ejecutable...
    echo [!bar!] !progress! / %total%
    timeout /t 1 >nul
    goto :progress_loop
)

:: Una vez finalizado
cls
echo Compilacion finalizada!.

SET "DEST=%CD%"

robocopy C:./dist/Presgen/ "%DEST%" /E /MOVE
rmdir /s /q .\dist\

pause

cls

echo Actualizacion Finalizada!
pause