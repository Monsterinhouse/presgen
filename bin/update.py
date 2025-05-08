import subprocess
import os

result = subprocess.run(
    ["git", "pull", "https://github.com/Monsterinhouse/presgen.git"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    os.system("cls")
    print("Actualización exitosa.")
    print (result.stdout)  # Opcional: mostrar la salida
    os.system("color 0a")
    print ("PresGen Actualizado Correctamente!")
else:
    print("Error al actualizar.")
    print(result.stderr)  # Opcional: mostrar el error
    os.system("color 0c")
