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

python ./update.py

rmdir ./temp_repo

:: Ejecuta pyinstaller en segundo plano
pyinstaller .\bin\main.py --specpath .\specs\ --name Presgen --icon .\media\PressGenLogo.png --onedir -y
pause

:: Simular barra de progreso mientras pyinstaller corre
set "total=50"
set /a progress=0

:progress_loop
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

cls
echo Compilacion finalizada!.
echo Actualizacion Completa!
pause
@REM echo testing pause
@REM pause

@REM SET DEST=%CD%

@REM :: Copia con sobreescritura forzada desde dist/Presgen/ al directorio actual
@REM rem robocopy ".\dist\Presgen\" "%DEST%" /E /MOVE /IS /IT /NFL /NDL /NJH /NJS

@REM :: Alternativa con XCOPY (comentada):
@REM echo %DEST%
@REM echo F | xcopy .\dist\Presgen\* %DEST%\ /E /Y /Q
@REM echo Copiado de archivos Completado

@REM rmdir /s /q .\dist\

@REM cls
@REM echo Actualizacion Finalizada
@REM pause