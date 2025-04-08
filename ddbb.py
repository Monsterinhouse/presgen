import sqlite3
import tkinter as tk
from tkinter import ttk, Toplevel

conn = sqlite3.connect('presdb.db')
cur = conn.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS clientes
            (id INTEGER PRIMARY KEY, pres_id INT, nombre TEXT, apellido TEXT, path TEXT, fecha TEXT)''')

def nventana() :
    ventana = Toplevel()
    ventana.title("Busqueda de Cliente")
    ventana.config(width= 300, height= 200, bg= "grey")

    framea = tk.Frame(ventana, width= 100, height= 100, borderwidth = 1, relief = "solid")

    l1 = ttk.Label(framea, text= "Nombre/Apellido: ")
    l2 = ttk.Label(framea, text= "ID: ")
    e1 = ttk.Entry(framea)
    e2 = ttk.Entry(framea)
    l1.grid (column= 0, row= 1, padx= 10, pady= 5)
    l2.grid (column= 2, row= 1, padx= 10, pady= 5)
    e1.grid (column= 1, row= 1, padx= 10, pady= 5)
    e2.grid (column= 3, row= 1, padx= 10, pady= 5)

    framea.grid(column= 0, row= 0, padx= 20, pady= 20)