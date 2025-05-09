import subprocess
import os
import shutil

REPO_URL = "https://github.com/Monsterinhouse/presgen.git"
TEMP_DIR = "temp_repo"

def es_repo_git():
    return os.path.isdir(".git")

def copiar_contenido(origen, destino):
    for item in os.listdir(origen):
        if item == ".git":
            continue  # Ignorar la carpeta .git completamente
        src_path = os.path.join(origen, item)
        dst_path = os.path.join(destino, item)

        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path, ignore_errors=True)  # Forzar borrado incluso si hay errores
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

# Limpia la consola y configura color
os.system("cls")
os.system("color 0a")

if es_repo_git():
    print("Repositorio detectado. Actualizando con git pull...")
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
else:
    print("No es un repositorio git. Clonando en carpeta temporal...")
    result = subprocess.run(["git", "clone", REPO_URL, TEMP_DIR], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Clonado exitosamente. Copiando archivos...")
        copiar_contenido(TEMP_DIR, ".")
        try:
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        except Exception as e:
            print(f"Error al eliminar carpeta temporal: {e}")
    else:
        os.system("color 0c")
        print("❌ Error al clonar el repositorio:")
        print(result.stderr)
        os.system("pause")
        exit()

# Mensaje final de éxito o error
if result.returncode == 0:
    print("\n✅ Actualización completada con éxito.")
    print(result.stdout)
else:
    os.system("color 0c")
    print("\n❌ Error durante la actualización.")
    print(result.stderr)

os.system("pause")
