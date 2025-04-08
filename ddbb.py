import sqlite3
import tkinter as tk
from tkinter import ttk, Toplevel

conn = sqlite3.connect('presdb.db')
cur = conn.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS clientes
            (id INTEGER PRIMARY KEY, pres_id INT, nombre TEXT, apellido TEXT, path TEXT, fecha TEXT)''')

def buscar() : 
    nya = str(e1.get())
    pid = e2.get()
    cur.execute("SELECT * FROM clientes WHERE nombre OR apellido = ? OR pres_id = ?", (nya, pid))
    fetch = cur.fetchall()
    for data in fetch :
        tree.insert ('', 'end', values=(data[2], data[3], data[4], data[5])) 
        
def nventana() :
    global e1, e2, tree
    ventana = Toplevel()
    ventana.title("Busqueda de Cliente")
    ventana.config(width= 300, height= 200, bg= "grey")

    framea = tk.Frame(ventana, width= 100, height= 100, borderwidth = 1, relief = "solid")

    # Buttons - Labels
    l1 = ttk.Label(framea, text= "Nombre/Apellido: ")
    l2 = ttk.Label(framea, text= "ID: ")
    e1 = ttk.Entry(framea)
    e2 = ttk.Entry(framea)
    b1  = ttk.Button(framea, text= "Buscar", command= buscar)
    b1.grid(column= 4, row= 1)

    # Tree
    headers = ("PID", "NOMBRE", "APELLIDO", "FECHA", "ARCHIVO")
    tree =  ttk.Treeview(framea, columns= headers, show= "headings")
    tree.heading("PID", text= "PID")
    tree.heading("NOMBRE", text= "NOMBRE")
    tree.heading("APELLIDO", text= "APELLIDO")
    tree.heading("FECHA", text= "FECHA")
    tree.heading("ARCHIVO", text= "ARCHIVO")
    tree.grid (row= 2, columnspan= 5, rowspan= 3, pady= 5, padx= 10)

    l1.grid (column= 0, row= 1, padx= 5, pady= 15)
    l2.grid (column= 2, row= 1, padx= 5, pady= 15)
    e1.grid (column= 1, row= 1, padx= 5, pady= 15)
    e2.grid (column= 3, row= 1, padx= 5, pady= 15)

    framea.grid(column= 0, row= 0, padx= 20, pady= 20)