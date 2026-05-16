import os
import sys
import subprocess
import requests

GITHUB_USER  = "Monsterinhouse"
GITHUB_REPO  = "presgen"
EXE_NAME     = "Presgen.exe"
VERSION_FILE = "last_version.txt"

API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"

def get_last_known_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            lineas = f.read().splitlines()
            return lineas[0].strip() if lineas else ""  # ← .strip() acá
    return ""

def save_version(tag, mensaje=""):
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(f"{tag}\n{mensaje}")

def check_and_update():
    os.system("cls")
    os.system("color 0a")
    print("Buscando actualizaciones...")

    try:
        response = requests.get(
            API_URL,
            headers={
                "User-Agent": "presgen-updater",
                "Cache-Control": "no-cache",  # ← headers anti-cache
                "Pragma": "no-cache"
            }
        )
        response.raise_for_status()
        release = response.json()

    except Exception as e:
        print(f"[X] No se pudo consultar GitHub: {e}")
        os.system("pause")
        return

    latest_tag = release["tag_name"].strip()  # ← .strip() acá
    last_known  = get_last_known_version()

    print(f"[DEBUG] Tag remoto raw: '{latest_tag}'")    # ← debugs
    print(f"[DEBUG] Version local raw: '{last_known}'")
    print(f"[DEBUG] Son iguales: {latest_tag == last_known}")

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
        temp_exe_path = os.path.abspath(temp_exe)
        bat_path = os.path.join(os.path.dirname(current_exe), "updater_temp.bat")
        
        with open(bat_path, "w") as bat:
             bat.write(f"""@echo off
timeout /t 2 /nobreak >nul
taskkill /f /im Presgen.exe >nul 2>&1
timeout /t 1 /nobreak >nul
del /f /q "{current_exe}"
move /y "{temp_exe_path}" "{current_exe}"
cd /d "{os.path.dirname(current_exe)}"
start "" "{current_exe}"
del "%~f0"
""")
            
        save_version(latest_tag, release.get("body", ""))
        print(f"\n[OK] Actualizacion a {latest_tag} completada. Relanzando...")
        # Correr el bat como administrador
        subprocess.Popen(
        ["powershell", "-Command",
        f"Start-Process -FilePath '{bat_path}' -Verb RunAs -WindowStyle Hidden"],
            shell=True
        )
        sys.exit(0)

    except Exception as e:
        print(f"[X] No se pudo reemplazar el ejecutable: {e}")
        os.system("pause")
        return

if __name__ == "__main__":
    print(f"[DEBUG] CWD: {os.getcwd()}")
    print(f"[DEBUG] __file__: {os.path.abspath(__file__)}")
    print(f"[DEBUG] EXE_NAME path: {os.path.abspath(EXE_NAME)}")
    print(f"[DEBUG] Presgen.exe existe: {os.path.exists(os.path.abspath(EXE_NAME))}")
    check_and_update()