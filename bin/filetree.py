import tkinter as tk
import ttkbootstrap as ttk
import os
from tkinter import filedialog

config_file = "./files/loadpath.txt"
filepath = 'Seleccione una carpeta...'
item_counter = 0  # Contador global

def get_unique_id():
    global item_counter
    item_counter += 1
    return f"item{item_counter}"

def guardar_ruta_config(path):
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(path)

def cargar_ruta_config():
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def seleccionar_o_cargar_ruta():
    ruta_guardada = cargar_ruta_config()
    if ruta_guardada and os.path.isdir(ruta_guardada):
        return ruta_guardada
    else:
        path = filedialog.askdirectory(title="Seleccionar carpeta principal")
        if path:
            guardar_ruta_config(path)
            return path
        else:
            return None

def folder():
    global item_counter
    item_counter = 0  # Reiniciar el contador

    path = seleccionar_o_cargar_ruta()
    if not path:
        return  # Si no se elige carpeta, salir de la función

    l1.config(text=path)

    for item in ftree.get_children():
        ftree.delete(item)

    # Carpetas principales
    for d in next(os.walk(path))[1]:
        carpeta_path = os.path.join(path, d)
        carpeta_id = get_unique_id()
        ftree.insert("", "end", iid=carpeta_id, values=[f'📁 {d}'])

        # Archivos en carpeta principal
        for f2 in next(os.walk(carpeta_path))[2]:
            ftree.insert(carpeta_id, 'end', iid=get_unique_id(), values=[f'   └ {f2}'])

        # Subcarpetas
        for sd in next(os.walk(carpeta_path))[1]:
            subcarpeta_path = os.path.join(carpeta_path, sd)
            subcarpeta_id = get_unique_id()
            ftree.insert(carpeta_id, 'end', iid=subcarpeta_id, values=[f'📂 {sd}'])

            for f3 in next(os.walk(subcarpeta_path))[2]:
                ftree.insert(subcarpeta_id, 'end', iid=get_unique_id(), values=[f'      └ {f3}'])

    # Archivos sueltos en la carpeta raíz
    for f in next(os.walk(path))[2]:
        ftree.insert("", "end", iid=get_unique_id(), values=[f])

def abrir(callback):
    def seleccionar_archivo():
        selected = ftree.selection()
        if selected:
            nombre = ftree.item(selected[0], "values")[0].strip()
            nombre = nombre.replace('📁', '').replace('📂', '').replace('└', '').strip()

            # Buscar la ruta del archivo seleccionado
            for root, dirs, files in os.walk(path_global):
                if nombre in files:
                    archivo_completo = os.path.join(root, nombre)
                    callback(archivo_completo)
                    roota.destroy()  # Cierra la ventana al seleccionar
                    return

    def mostrar_ventana(callback_fn):
        global l1, ftree, path_global, roota
        roota = tk.Tk()
        roota.title("Abrir...")

        # Seleccionar carpeta al inicio
        path_global = seleccionar_o_cargar_ruta()
        if not path_global:
            roota.destroy()
            return

        # Crear la interfaz gráfica
        b1 = ttk.Button(roota, text="Seleccionar Carpeta", command=folder, bootstyle="warning")
        l1 = ttk.Label(roota, text=path_global, relief="solid", padding=5)
        b2 = ttk.Button(roota, text="Abrir", command=seleccionar_archivo, bootstyle="success")
        ftree = ttk.Treeview(roota, selectmode="browse", bootstyle="dark", height=30)

        ftree["columns"] = ("1")
        ftree["show"] = "tree headings"
        ftree.column("#0", anchor="c", width=20)
        ftree.column("1", anchor="w", width=300)
        ftree.heading("#0", text="#")
        ftree.heading("1", text="Nombre", anchor="w")

        b1.grid(row=0, column=0, pady=10, padx=10)
        b2.grid(row=2, column=1, pady=10, padx=10)
        l1.grid(row=0, column=1, pady=10, padx=10)
        ftree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Llamar a folder() para cargar los archivos y carpetas al treeview
        folder()

        # Iniciar la ventana
        roota.mainloop()

    # Llamar a la función mostrar_ventana pasando el callback
    mostrar_ventana(callback)
