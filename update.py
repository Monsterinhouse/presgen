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

API_URL      = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases"

def get_last_known_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            lineas = f.read().splitlines()
            return lineas[0] if lineas else ""
    return ""

def save_version(tag, mensaje=""):
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(f"{tag}\n{mensaje}")

def check_and_update():
    os.system("cls")
    os.system("color 0a")
    print("Buscando actualizaciones...")

    try:
        response = requests.get(API_URL, headers={"User-Agent": "presgen-updater"})
        response.raise_for_status()
        releases = response.json()
        if not releases:
            print("[!] No hay releases disponibles todavía.")
            os.system("pause")
            return
        release = releases[0]  # el más reciente
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

    save_version(latest_tag, release.get("body", ""))
    print(f"\n[200] Actualización a {latest_tag} completada con éxito.")
    os.system("timeout 10")

if __name__ == "__main__":
    check_and_update()