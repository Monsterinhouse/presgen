@ECHO OFF

cls
echo "Al apretar Enter, se actualizara la aplicacion"
pause

SET gp = git pull

if gp == 0 (
    cls
    echo "Actualizando..."
    %gp%
) else (
    cls
    echo "No se pudo actualizar. Quiza su version es la mas reciente"
    pause 
)