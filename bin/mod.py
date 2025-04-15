import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os

ARCHIVO = "./files/repuestos.csv"

# Cargar CSV
if not os.path.exists(ARCHIVO):
    df = pd.DataFrame(columns=["repuesto", "precio"])
    df.to_csv(ARCHIVO, index=False)

def cargar_datos():
    return pd.read_csv(ARCHIVO)

def guardar_datos(df):
    df.to_csv(ARCHIVO, index=False)


def mostrar():
    df = cargar_datos()
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, df.to_string(index=False))

def crear():
    df = cargar_datos()
    nombre = e_nombre.get().strip()
    if nombre in df['repuesto'].values:
        messagebox.showerror("Error", "El repuesto ya existe.")
        return
    try:
        precio_str = e_precio.get().strip()
        precio_str = precio_str.replace(",", ".")
        precio_str = ''.join(c for c in precio_str if c.isdigit() or c == '.')
        precio = float(precio_str)
        nuevo = pd.DataFrame([{"repuesto": nombre, "precio": precio}])
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar_datos(df)
        limpiar()
        messagebox.showinfo("Éxito", "Repuesto agregado.")
    except Exception as e:
        messagebox.showerror("Error", f"Precio inválido. {e}")

def actualizar():
    df = cargar_datos()
    nombre = e_nombre.get().strip()
    if nombre not in df['repuesto'].values:
        messagebox.showerror("Error", "El repuesto no existe.")
        return
    try:
        precio = float(e_precio.get())
        df.loc[df['repuesto'].str.strip() == nombre, 'precio'] = float(precio)
        guardar_datos(df)
        limpiar()
        mostrar()
        messagebox.showinfo("Éxito", "Repuesto actualizado.")
    except:
        messagebox.showerror("Error", "Precio inválido.")

def eliminar():
    df = cargar_datos()
    nombre = e_nombre.get().strip()
    if nombre not in df['repuesto'].values:
        messagebox.showerror("Error", "El repuesto no existe.")
        return
    df = df[df['repuesto'] != nombre]
    guardar_datos(df)
    limpiar()
    mostrar()
    messagebox.showinfo("Éxito", "Repuesto eliminado.")

def limpiar():
    e_nombre.delete(0, tk.END)
    e_precio.delete(0, tk.END)

def app() :
    global root, e_nombre, e_precio, text_area
    # GUI
    root = tk.Tk()
    root.title("CRUD - Repuestos CSV")
    root.geometry("500x500")

    ttk.Label(root, text="Repuesto").pack()
    e_nombre = tk.Entry(root)
    e_nombre.pack()

    ttk.Label(root, text="Precio").pack()
    e_precio = tk.Entry(root)
    e_precio.pack()

    ttk.Button(root, text="Agregar", command=crear).pack(pady=5)
    ttk.Button(root, text="Actualizar", command=actualizar).pack(pady=5)
    ttk.Button(root, text="Eliminar", command=eliminar).pack(pady=5)
    ttk.Button(root, text="Mostrar Todos", command=mostrar).pack(pady=5)

    text_area = tk.Text(root, height=15, width=60)
    text_area.pack(pady=10)

    mostrar()

    root.mainloop()

def verificar_contraseña():
    password = entry_pass.get()
    if password == "LDNJRTZHHJYX27011833":  # <-- Cambiá esto si querés otra contraseña
        login.destroy()
        app()
    else:
        messagebox.showerror("Acceso denegado", "Contraseña incorrecta.")
        login.destroy()
        exit()

login = tk.Tk()
login.title("Ingreso al sistema")
login.geometry("300x150")
login.resizable(False, False)

ttk.Label(login, text="Ingrese la contraseña:").pack(pady=10)
entry_pass = ttk.Entry(login, show="*")
entry_pass.pack()
ttk.Button(login, text="Ingresar", command=verificar_contraseña).pack(pady=10)

login.mainloop()
