import tkinter as tk
from tkinter import ttk

# SystemConfig
app = tk.Tk()
app.geometry ("600x400")
app.title ("PresGen V1.1")
app.config (bg="grey")

# Frame(s)
frame1 = tk.Frame (app, width = 100, height = 100, borderwidth = 1, relief = "solid")
frame2 = tk.Frame (app)

# Labels
l1 = tk.Label(frame1, text = "Nombre: ")
l2 = tk.Label(frame1, text = "Apellido: ")
l3 = tk.Label(frame1, text = "Domicilio: ")
l4 = tk.Label(frame1, text = "Telefono: ")
l5 = tk.Label(frame1, text = "Vehiculo: ")
l6 = tk.Label(frame1, text = "Marca: ")
l7 = tk.Label(frame1, text = "Modelo: ")
l8 = tk.Label(frame1, text = "N° Motor: ")
l9 = tk.Label(frame1, text = "N° de Chasis: ")
l10 = tk.Label(frame1, text = "Dominio: ")

l1.grid(row= 0, column= 0, padx = 10, pady = 5)
l2.grid(row= 1, column= 0, padx = 10, pady = 5)
l3.grid(row= 2, column= 0, padx = 10, pady = 5)
l4.grid(row= 3, column= 0, padx = 10, pady = 5)
l5.grid(row= 4, column= 0, padx = 10, pady = 5)
l6.grid(row= 5, column= 0, padx = 10, pady = 5)
l7.grid(row= 6, column= 0, padx = 10, pady = 5)
l8.grid(row= 7, column= 0, padx = 10, pady = 5)
l9.grid(row= 8, column= 0, padx = 10, pady = 5)
l10.grid(row= 9, column= 0, padx = 10, pady = 5)

# Entrys


# Frame-Packs
frame1.pack(side = "left", padx = 20, pady = 20)

app.mainloop()