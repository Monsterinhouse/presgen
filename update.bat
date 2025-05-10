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

color 0a

rmdir /s /q build
rmdir /s /q dist
rm specs/Presgen.spec

:: Ejecuta pyinstaller en segundo plano
pyinstaller .\bin\main.py --specpath .\specs\ --name Presgen --icon .\media\PressGenLogo.png --onedir -y

:: Copiar los archivos generados desde dist\Presgen\ al directorio actual, sobrescribiendo
robocopy ".\dist\Presgen" "." /E /MOVE /IS /IT /NFL /NDL /NJH /NJS

:: Eliminar carpeta dist
rmdir /s /q .\dist

cls
echo Compilacion finalizada!.
echo Actualizacion Completa!
pause
