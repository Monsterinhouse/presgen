import subprocess
import os
import shutil
import stat

REPO_URL = "https://github.com/Monsterinhouse/presgen.git"
TEMP_DIR = "temp_repo"

def es_repo_git():
    return os.path.isdir(".git")

def copiar_contenido(origen, destino):
    for item in os.listdir(origen):
        if item == ".git":
            continue
        src_path = os.path.join(origen, item)
        dst_path = os.path.join(destino, item)

        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path, ignore_errors=True)
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

def force_remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Limpia consola
os.system("cls")
os.system("color 0a")

if es_repo_git():
    print("Repositorio detectado. Actualizando con git pull...")
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
else:
    print("No es un repositorio git. Clonando en carpeta temporal...")
    if os.path.exists(TEMP_DIR):
        print("[!] Carpeta temporal existente. Eliminando antes de clonar...")
        try:
            shutil.rmtree(TEMP_DIR, onerror=force_remove_readonly)
        except Exception as e:
            print(f"[X] No se pudo eliminar '{TEMP_DIR}': {e}")
            os.system("pause")
            exit()

    result = subprocess.run(["git", "clone", REPO_URL, TEMP_DIR], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Clonado exitosamente. Copiando archivos...")
        copiar_contenido(TEMP_DIR, ".")
        try:
            shutil.rmtree(TEMP_DIR, onerror=force_remove_readonly)
        except Exception as e:
            print(f"[!] No se pudo eliminar la carpeta temporal '{TEMP_DIR}': {e}")
    else:
        os.system("color 0c")
        print("[X] Error al clonar el repositorio:")
        print(result.stderr)
        os.system("pause")
        exit()

if result.returncode == 0:
    print("\n[200] Actualización completada con éxito.")
    print(result.stdout)
else:
    os.system("color 0c")
    print("\n[X] Error durante la actualización.")
    print(result.stderr)

os.system("pause")
