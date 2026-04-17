# import subprocess
# import os
# import shutil
# import stat

# REPO_URL = "https://github.com/Monsterinhouse/presgen.git"
# TEMP_DIR = "temp_repo"

# def es_repo_git():
#     return os.path.isdir(".git")

# def copiar_contenido(origen, destino):
#     for item in os.listdir(origen):
#         if item == ".git":
#             continue
#         src_path = os.path.join(origen, item)
#         dst_path = os.path.join(destino, item)

#         if os.path.isdir(src_path):
#             if os.path.exists(dst_path):
#                 shutil.rmtree(dst_path, ignore_errors=True)
#             shutil.copytree(src_path, dst_path)
#         else:
#             shutil.copy2(src_path, dst_path)

# def force_remove_readonly(func, path, excinfo):
#     os.chmod(path, stat.S_IWRITE)
#     func(path)

# # Limpia consola
# os.system("cls")
# os.system("color 0a")

# if es_repo_git():
#     print("Repositorio detectado. Actualizando con git pull...")
#     result = subprocess.run(["git", "pull"], capture_output=True, text=True)
# else:
#     print("No es un repositorio git. Clonando en carpeta temporal...")
#     if os.path.exists(TEMP_DIR):
#         print("[!] Carpeta temporal existente. Eliminando antes de clonar...")
#         try:
#             shutil.rmtree(TEMP_DIR, onerror=force_remove_readonly)
#         except Exception as e:
#             print(f"[X] No se pudo eliminar '{TEMP_DIR}': {e}")
#             os.system("pause")
#             exit()

#     result = subprocess.run(["git", "clone", REPO_URL, TEMP_DIR], capture_output=True, text=True)
    
#     if result.returncode == 0:
#         print("Clonado exitosamente. Copiando archivos...")
#         copiar_contenido(TEMP_DIR, ".")
#         try:
#             shutil.rmtree(TEMP_DIR, onerror=force_remove_readonly)
#         except Exception as e:
#             print(f"[!] No se pudo eliminar la carpeta temporal '{TEMP_DIR}': {e}")
#     else:
#         os.system("color 0c")
#         print("[X] Error al clonar el repositorio:")
#         print(result.stderr)
#         os.system("pause")
#         exit()

# if result.returncode == 0:
#     print("\n[200] Actualización completada con éxito.")
#     print(result.stdout)
    
# else:
#     os.system("color 0c")
#     print("\n[X] Error durante la actualización.")
#     print(result.stderr)

# os.system("timeout 10")

import os
import sys
import stat
import shutil
import subprocess
import requests  # pip install requests

GITHUB_USER  = "Monsterinhouse"
GITHUB_REPO  = "presgen"
EXE_NAME     = "Presgen.exe"
VERSION_FILE = "last_version.txt"  # Guarda el SHA del último build

API_URL      = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"

def get_last_known_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_version(tag):
    with open(VERSION_FILE, "w") as f:
        f.write(tag)

def check_and_update():
    os.system("cls")
    os.system("color 0a")
    print("Buscando actualizaciones...")

    try:
        response = requests.get(API_URL, headers={"User-Agent": "presgen-updater"})
        response.raise_for_status()
        release = response.json()
    except Exception as e:
        print(f"[X] No se pudo consultar GitHub: {e}")
        os.system("pause")
        return

    latest_tag = release["tag_name"]
    last_known  = get_last_known_version()

    if latest_tag == last_known:
        print(f"[OK] Ya tenés la última versión ({latest_tag}).")
        os.system("timeout 5")
        return

    # Hay versión nueva
    print(f"[!] Nueva versión encontrada: {latest_tag}")
    print(f"    Cambios: {release.get('body', 'Sin descripción')}")
    print("Descargando...")

    # Buscar el .exe entre los assets del release
    asset_url = None
    for asset in release.get("assets", []):
        if asset["name"] == EXE_NAME:
            asset_url = asset["browser_download_url"]
            break

    if not asset_url:
        print("[X] No se encontró el ejecutable en el release.")
        os.system("pause")
        return

    # Descargar el nuevo .exe
    try:
        dl = requests.get(asset_url, stream=True)
        dl.raise_for_status()
        temp_exe = EXE_NAME + ".new"
        with open(temp_exe, "wb") as f:
            for chunk in dl.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"[X] Error al descargar: {e}")
        os.system("pause")
        return

    # Reemplazar el .exe actual
    try:
        if os.path.exists(EXE_NAME):
            os.remove(EXE_NAME)
        os.rename(temp_exe, EXE_NAME)
    except Exception as e:
        print(f"[X] No se pudo reemplazar el ejecutable: {e}")
        os.system("pause")
        return

    save_version(latest_tag)
    print(f"\n[200] Actualización a {latest_tag} completada con éxito.")
    os.system("timeout 10")

if __name__ == "__main__":
    check_and_update()