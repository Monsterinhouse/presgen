import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os

ARCHIVO = "./files/repuestos.csv"

# Lista de nombres prohibidos que no son repuestos
PROHIBIDOS = {"MANO DE OBRA", "SERVICIO", "MO", "MANO OBRA", "SERVICIOS"}

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    df = pd.DataFrame(columns=["repuestos"])
    df.to_csv(ARCHIVO, index=False)

def es_valido(nombre):
    return nombre.upper() not in PROHIBIDOS and nombre.strip() != ""

def cargar_datos():
    return pd.read_csv(ARCHIVO)

def guardar_datos(df):
    df.to_csv(ARCHIVO, index=False)

def mostrar():
    df = cargar_datos()
    text_area.delete("1.0", tk.END)
    if df.empty:
        text_area.insert(tk.END, "No hay repuestos cargados.")
    else:
        text_area.insert(tk.END, df.to_string(index=False))

def crear():
    df = cargar_datos()
    nombre = e_nombre.get().strip()
    if not es_valido(nombre):
        messagebox.showerror("Error", "Nombre de repuesto inválido o reservado.")
        return
    if nombre in df['repuestos'].values:
        messagebox.showerror("Error", "El repuesto ya existe.")
        return
    nuevo = pd.DataFrame([{"repuestos": nombre}])
    df = pd.concat([df, nuevo], ignore_index=True)
    guardar_datos(df)
    limpiar()
    messagebox.showinfo("Éxito", "Repuesto agregado.")
    mostrar()

def actualizar():
    df = cargar_datos()
    nombre = e_nombre.get().strip()
    if not es_valido(nombre):
        messagebox.showerror("Error", "Nombre de repuestos inválido o reservado.")
        return
    if nombre not in df['repuestos'].values:
        messagebox.showerror("Error", "El repuesto no existe.")
        return
    # Simulación: eliminar y volver a agregar (ya que no hay más campos)
    df = df[df['repuestos'] != nombre]
    df = pd.concat([df, pd.DataFrame([{"repuestos": nombre}])], ignore_index=True)
    guardar_datos(df)
    limpiar()
    messagebox.showinfo("Éxito", "Repuesto actualizado.")
    mostrar()

def eliminar():
    df = cargar_datos()
    nombre = e_nombre.get().strip()
    if nombre not in df['repuestos'].values:
        messagebox.showerror("Error", "El repuesto no existe.")
        return
    df = df[df['repuestos'] != nombre]
    guardar_datos(df)
    limpiar()
    messagebox.showinfo("Éxito", "Repuesto eliminado.")
    mostrar()

def limpiar():
    e_nombre.delete(0, tk.END)

def app():
    global root, e_nombre, text_area
    root = tk.Tk()
    root.title("CRUD - repuestos CSV")
    root.geometry("500x450")

    ttk.Label(root, text="Nombre del repuestos").pack()
    e_nombre = tk.Entry(root)
    e_nombre.pack(pady=5)

    ttk.Button(root, text="Agregar", command=crear).pack(pady=5)
    ttk.Button(root, text="Actualizar", command=actualizar).pack(pady=5)
    ttk.Button(root, text="Eliminar", command=eliminar).pack(pady=5)
    ttk.Button(root, text="Mostrar Todos", command=mostrar).pack(pady=5)

    text_area = tk.Text(root, height=15, width=60)
    text_area.pack(pady=10)

    mostrar()

    root.mainloop()

app()

app.mainloop()
