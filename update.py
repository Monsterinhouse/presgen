import os
import sys
import subprocess
import requests

GITHUB_USER  = "Monsterinhouse"
GITHUB_REPO  = "presgen"
EXE_NAME     = "Presgen.exe"
VERSION_FILE = "last_version.txt"

API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases"

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

        # Filtrar solo releases publicados (no draft, no prerelease)
        releases = [r for r in releases if not r.get("draft") and not r.get("prerelease")]

        if not releases:
            print("[!] No hay releases disponibles todavía.")
            os.system("pause")
            return

        release = releases[0]  # el más reciente publicado

    except Exception as e:
        print(f"[X] No se pudo consultar GitHub: {e}")
        os.system("pause")
        return

    latest_tag = release["tag_name"]
    last_known  = get_last_known_version()

    print(f"    Ultima version remota : {latest_tag}")
    print(f"    Version local         : {last_known}")

    if latest_tag == last_known:
        print(f"[OK] Ya tenes la ultima version ({latest_tag}).")
        os.system("timeout 5")
        return

    # Hay version nueva
    print(f"[!] Nueva version encontrada: {latest_tag}")
    print(f"    Cambios: {release.get('body', 'Sin descripcion')}")
    print("Descargando...")

    # Buscar el .exe entre los assets
    asset_url = None
    for asset in release.get("assets", []):
        if asset["name"] == EXE_NAME:
            asset_url = asset["browser_download_url"]
            break

    if not asset_url:
        print(f"[X] No se encontro '{EXE_NAME}' en el release.")
        print("    Assets disponibles:")
        for asset in release.get("assets", []):
            print(f"      - {asset['name']}")
        os.system("pause")
        return

    # Descargar
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

    # Reemplazar con .bat para evitar el WinError 5
    try:
        current_exe = os.path.abspath(EXE_NAME)
        bat_path = os.path.join(os.path.dirname(current_exe), "updater_temp.bat")
        with open(bat_path, "w") as bat:
            bat.write(f"""@echo off
timeout /t 2 /nobreak >nul
del "{current_exe}"
move "{os.path.abspath(temp_exe)}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
""")
        save_version(latest_tag, release.get("body", ""))
        print(f"\n[OK] Actualizacion a {latest_tag} completada. Relanzando...")
        subprocess.Popen(bat_path, shell=True)
        sys.exit(0)

    except Exception as e:
        print(f"[X] No se pudo reemplazar el ejecutable: {e}")
        os.system("pause")
        return

if __name__ == "__main__":
    check_and_update()