import tkinter as tk
from tkinter import ttk, messagebox

# SystemConfig
app = tk.Tk()
app.geometry ("1500x600")
app.title ("PresGen V1.1")
app.config (bg="grey")

# Varibles / Lists / Misc
repuestos = []
pres_list = []
precios = {}

with open("./files/repuestos.csv") as csv_file:
    for line in csv_file:
        data = line.strip().split(',')
        if len(data) == 2:  # Asegurar que hay dos elementos (nombre y precio)
            repuestos.append(data[0])  # Agregar el nombre del repuesto
            precios[data[0]] = data[1]  # Guardar precio asociado al repuesto


def upd_precio(event):
    rs = e12.get()  # Obtener el repuesto seleccionado
    precio = precios.get(rs, "N/A")  # Obtener el precio o 'N/A' si no existe
    ep.delete(0, tk.END)  # Borrar el contenido previo
    ep.insert(0, precio)  # Insertar el nuevo precio

def clear_item() :
    e11.delete(0, tk.END)
    e12.delete(0, tk.END)
    ep.delete(0, tk.END)
    e13.delete(0, tk.END)

def add_item() :
    try: 
        cantidad = int(e11.get())
        repuestos = e12.get()
        unitario = float(ep.get())
        ab = e13.get()
        precio = unitario * cantidad
        pres_items = [cantidad, repuestos, unitario, ab, precio]
        tree.insert('', 0, values = pres_items)
        clear_item()
    
    except ValueError:
        messagebox.showinfo(message = "Tenes que ingresar todos los valores!", title = "AVISO!")
    
    pres_list.append(pres_items)

# Frame(s)
frame1 = tk.Frame (app, width = 100, height = 100, borderwidth = 1, relief = "solid")
frame2 = tk.Frame (app, width = 800, height = 800, borderwidth = 1, relief = "solid")

# Labels - Info
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

l1.grid(row= 0, column= 0, padx = 10, pady = 10)
l2.grid(row= 1, column= 0, padx = 10, pady = 5)
l3.grid(row= 2, column= 0, padx = 10, pady = 5)
l4.grid(row= 3, column= 0, padx = 10, pady = 5)
l5.grid(row= 4, column= 0, padx = 10, pady = 5)
l6.grid(row= 5, column= 0, padx = 10, pady = 5)
l7.grid(row= 6, column= 0, padx = 10, pady = 5)
l8.grid(row= 7, column= 0, padx = 10, pady = 5)
l9.grid(row= 8, column= 0, padx = 10, pady = 5)
l10.grid(row= 9, column= 0, padx = 10, pady = 10)

# Labels - Datos
l11 = tk.Label(frame2, text = "Cantidad: ")
l12 = tk.Label(frame2, text = "Repuesto: ")
l13 = tk.Label(frame2, text = "Precio:")

l11.grid(row= 0, column= 1, padx = 10, pady = 5)
l12.grid(row= 0, column= 2, padx = 10, pady = 5)
l13.grid(row= 0, column= 3, padx = 10, pady = 5)

# Entry - Info
e1 = ttk.Entry(frame1)
e2 = ttk.Entry(frame1)
e3 = ttk.Entry(frame1)
e4 = ttk.Entry(frame1)
e5 = ttk.Entry(frame1)
e6 = ttk.Entry(frame1)
e7 = ttk.Entry(frame1)
e8 = ttk.Entry(frame1)
e9 = ttk.Entry(frame1)
e10 = ttk.Entry(frame1)

e1.grid(row= 0, column= 1, padx = 10, pady = 5)
e2.grid(row= 1, column= 1, padx = 10, pady = 5)
e3.grid(row= 2, column= 1, padx = 10, pady = 5)
e4.grid(row= 3, column= 1, padx = 10, pady = 5)
e5.grid(row= 4, column= 1, padx = 10, pady = 5)
e6.grid(row= 5, column= 1, padx = 10, pady = 5)
e7.grid(row= 6, column= 1, padx = 10, pady = 5)
e8.grid(row= 7, column= 1, padx = 10, pady = 5)
e9.grid(row= 8, column= 1, padx = 10, pady = 5)
e10.grid(row= 9, column= 1, padx = 10, pady = 5)

# Entry - Datos
e11 = ttk.Entry(frame2)
e12 = ttk.Combobox(frame2, values= repuestos)
e12.bind("<<ComboboxSelected>>", upd_precio)
e11.grid(row= 1, column= 1, padx = 10, pady = 5)
e12.grid(row= 1, column= 2, padx = 10, pady = 5)

ep = ttk.Entry(frame2)
ep.grid(row= 1, column= 3, padx = 10, pady = 5)
el = tk.Label(frame2, text="Estado:")
el.grid(row= 0, column= 4, padx = 10, pady = 5)
ee = ttk.Combobox(frame2, values= ["A: Reponer", "B: Reparar"])
ee.grid(row= 1, column= 4, padx = 10, pady = 5)

# Treeview
headers = ("Cantidad", "Repuestos", "Unitario", "A/B", "Total")
tree = ttk.Treeview(frame2, columns=headers, show="headings")
tree.heading("Cantidad", text="Cantidad")
tree.heading("Repuestos", text="Repuestos")
tree.heading("Unitario", text="Unitario")
tree.heading("A/B", text="A/B")
tree.heading("Total", text="Total")
tree.grid (row = 2, columnspan = 6, pady = 10, padx = 10)
addb = ttk.Button(frame2, text = "Agregar", command = add_item)
addb.grid(row= 2, column= 6, padx = 10, pady = 10)

# Frame-Packs
frame1.pack(side = "left", padx = 20, pady = 20)
frame2.pack(side = "right", padx = 20, pady = 20)

app.mainloop()