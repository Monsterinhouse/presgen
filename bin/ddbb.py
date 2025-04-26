import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
import os
from tkinter import Toplevel, messagebox
from docx2pdf import convert

conn = sqlite3.connect('./files/presdb.db')
cur = conn.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS clientes
            (id INTEGER PRIMARY KEY, pres_id INT, nombre TEXT, apellido TEXT, path TEXT, fecha TEXT)''')

def caps(event) :
    caps.set(caps.get().upper())

def buscar() :
    tree.delete(*tree.get_children())
    try:
        nya = str(e1.get())
        pid = e2.get()
        cur.execute("SELECT * FROM clientes WHERE nombre OR apellido = ? OR pres_id = ?", (nya, pid))
        fetch = cur.fetchall()
        for data in fetch :
            tree.insert ('', 'end', values=(data[1], data[2], data[3], data[5], data[4])) 
    
    except ValueError:
        messagebox.showinfo(message = "Ingresa un parametro de busqueda!", title = "AVISO!") 

def abrir() :
    try:
        item = tree.selection()[0]
        item_data = tree.item(item, "values")
        path = item_data[4]
        if path:
            os.startfile(path)
        else:
            messagebox.showinfo(message="No hay archivo asociado.", title="AVISO!")
    except IndexError:
        messagebox.showinfo(message="Selecciona un elemento de la lista.", title="AVISO!")
        
def nventana() :
    global e1, e2, tree
    ventana = Toplevel()
    ventana.title("Busqueda de Cliente/Presupuesto")
    ventana.config(bg= "grey")
    framea = tk.Frame(ventana, borderwidth = 1, relief = "solid")
    
    # Buttons - Labels
    l1 = ttk.Label(framea, text= "Nombre/Apellido: ")
    l2 = ttk.Label(framea, text= "ID: ")
    e1 = ttk.Entry(framea, textvariable= caps, bootstyle= "dark")
    e2 = ttk.Entry(framea, textvariable= caps, bootstyle= "dark")
    b1 = ttk.Button(framea, text= "Buscar Cliente/Presupuesto", command= buscar)
    b2 = ttk.Button(framea, text= "Abrir Presupuesto", command= abrir)
    b1.grid(column= 4, row= 1)
    b2.grid(column= 4, row= 6, pady= 5)

    # Tree
    headers = ("PID", "NOMBRE", "APELLIDO", "FECHA", "ARCHIVO")
    tree =  ttk.Treeview(framea, columns= headers, show= "headings", bootstyle= "dark")
    tree.heading("PID", text= "PID", anchor="center")
    tree.column("PID", width= 100, anchor="center")
    tree.heading("NOMBRE", text= "NOMBRE", anchor="center")
    tree.column("NOMBRE", width= 100, anchor="center")
    tree.heading("APELLIDO", text= "APELLIDO", anchor="center")
    tree.column("APELLIDO", width= 100, anchor="center")
    tree.heading("FECHA", text= "FECHA", anchor="center")
    tree.column("FECHA", width= 100, anchor="center")
    tree.heading("ARCHIVO", text= "ARCHIVO", anchor="center")
    tree.column("ARCHIVO", width= 500, anchor="center")
    tree.grid (row= 2, columnspan= 5, rowspan= 3, pady= 5, padx= 10)

    l1.grid (column= 0, row= 1, padx= 5, pady= 15)
    l2.grid (column= 2, row= 1, padx= 5, pady= 15)
    e1.grid (column= 1, row= 1, padx= 5, pady= 15)
    e2.grid (column= 3, row= 1, padx= 5, pady= 15)
    l1.grid (column= 0, row= 1, padx= 10, pady= 5)
    l2.grid (column= 2, row= 1, padx= 10, pady= 5)
    e1.grid (column= 1, row= 1, padx= 10, pady= 5)
    e2.grid (column= 3, row= 1, padx= 10, pady= 5)

    framea.grid(column= 0, row= 0, padx= 20, pady= 20)