import tkinter as tk
import datetime, os
import sqlite3
from docxtpl import DocxTemplate
from docx2pdf import convert
from tkinter import ttk, messagebox, filedialog 
from pathlib import Path
from ddbb import nventana

# DDBB Conx
conn = sqlite3.connect('presdb.db')
cur = conn.cursor()

def query() :
    values = ('''INSERT INTO clientes (pres_id, nombre, apellido, path, fecha)
                VALUES (?, ?, ?, ?, ?)''')
    d_tuple = (pid, e1.get().upper(), e2.get().upper(), doc_path, t.strftime("%d/%m/%Y"))
    cur.execute(values, d_tuple)
    conn.commit()
    cur.close()

# SystemConfig
app = tk.Tk()
app.geometry ("1500x600")
app.title ("PresGen V1.0")
app.config (bg="grey")

# Varibles / Lists / Misc
idfile = Path("./files/id.txt")
t = datetime.datetime.now()
pid = 0
repuestos = []
pres_list = []
precios = {}
caps = str()

def caps(event) :
    caps.set(caps.get().upper())

with open("./files/repuestos.csv", encoding='utf-8', errors='ignore') as csv_file:
    next(csv_file)
    for line in csv_file:
        data = line.strip().split(',')
        if len(data) == 2:  # Asegurar que hay dos elementos (nombre y precio)
            repuestos.append(data[0])  # Agregar el nombre del repuesto
            precios[data[0]] = data[1]  # Guardar precio asociado al repuesto

if os.path.exists(idfile):
    with open(idfile, "r", encoding="utf-8") as f:
        content = f.read().strip()
        pid = int(content) if content.isdigit() else 0
else: 
    with open(idfile, "w", encoding="utf-8") as f:
        f.write('0')
        pid = 0

def upd_precio(event):
    rs = e12.get()  # Obtener el repuesto seleccionado
    precio = precios.get(rs, "N/A")  # Obtener el precio o 'N/A' si no existe
    ep.delete(0, tk.END)  # Borrar el contenido previo
    ep.insert(0, precio)  # Insertar el nuevo precio

def clear_item() :
    e11.delete(0, tk.END)
    e12.delete(0, tk.END)
    ep.delete(0, tk.END)
    ee.delete(0, tk.END)

def new_pres() :
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)
    e6.delete(0, tk.END)
    e7.delete(0, tk.END)
    e8.delete(0, tk.END)
    e9.delete(0, tk.END)
    e10.delete(0, tk.END)
    e11.delete(0, tk.END)
    e12.delete(0, tk.END)
    ep.delete(0, tk.END)
    ee.delete(0, tk.END)
    clear_item()
    tree.delete(*tree.get_children())

    pres_list.clear()

def add_item() :
    try: 
        cantidad = int(e11.get())
        repuestos = e12.get()
        unitario = float(ep.get())
        ab = ee.get()
        precio = unitario * cantidad
        pres_items = [cantidad, repuestos, unitario, ab, precio]
        tree.insert('', 0, values = pres_items)
        clear_item()
    
    except ValueError:
        messagebox.showinfo(message = "Tenes que ingresar todos los valores!", title = "AVISO!")
    
    pres_list.append(pres_items)

def gen_pres() :
    global pid, eid, doc_path
    doc = DocxTemplate("./files/Pres_Template.docx")
    nya = e1.get().upper() + " " + e2.get().upper()
    domicilio = e3.get().upper()
    telefono = e4.get()
    vehiculo = e5.get().upper()
    marca = e6.get().upper()
    modelo = e7.get().upper()
    nmotor = e8.get()
    nchasis = e9.get()
    dominio = e10.get()
    pid = pid
    d = t.strftime("%d")
    m = t.strftime("%m")
    y = t.strftime("%Y")
    subtotal = sum(item[4] for item in pres_list)
    total = subtotal * 1.21 

    doc.render({"nya": nya,
               "domicilio": domicilio,
               "telefono": telefono,
               "vehiculo": vehiculo,
               "marca": marca,
               "modelo": modelo,
               "nmotor": nmotor,
               "nchasis": nchasis,
               "dominio": dominio,
               "subtotal": subtotal,
               "total": total,
               "pid": pid,
               "d": d,
               "m": m,
               "y": y,
               "pres_list": pres_list
                })
    
    messagebox.showinfo("AVISO!", "Seleccione la carpeta donde desea guardar los presupuestos")
    file = filedialog.askdirectory()

    if not file:
        messagebox.showwarning("AVISO!", "No se selecciono una carpeta")
        return


    doc_name = f"Presupuesto_{str(pid)}_{nya}_{t.strftime('%d-%m-%Y-%H%M%S')}.docx"
    doc_path = os.path.join(file, doc_name)
    doc.save(doc_path)
    convert(doc_path, doc_path.replace(".docx", ".pdf"))
    os.remove(doc_path)
    messagebox.showinfo("!!!AVISO!!!", "Presupuesto Generado!")
    
    pid += 1

    with open(idfile, "w", encoding="utf-8") as f:
        f.write(str(pid))

    eid.delete(0, tk.END)
    eid.insert(0, pid)

    query()
    new_pres()

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
e1 = ttk.Entry(frame1, textvariable= caps)
e2 = ttk.Entry(frame1, textvariable= caps)
e3 = ttk.Entry(frame1, textvariable= caps)
e4 = ttk.Entry(frame1)
e5 = ttk.Entry(frame1, textvariable= caps)
e6 = ttk.Entry(frame1, textvariable= caps)
e7 = ttk.Entry(frame1)
e8 = ttk.Entry(frame1)
e9 = ttk.Entry(frame1)
e10 = ttk.Entry(frame1, textvariable= caps)
bb = ttk.Button(frame1, text= "Buscar", command= nventana)

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
bb.grid(row= 10, column= 1, padx = 10, pady = 5)

# Entry - Datos
e11 = ttk.Entry(frame2)
e12 = ttk.Combobox(frame2, width= 30, values= repuestos)
e12.bind("<<ComboboxSelected>>", upd_precio)
e12.configure(state='readonly')
e11.grid(row= 1, column= 1, padx = 10, pady = 5)
e12.grid(row= 1, column= 2, padx = 10, pady = 5)

ep = ttk.Entry(frame2)
ep.grid(row= 1, column= 3, padx = 10, pady = 5)
le = tk.Label(frame2, text="Estado:")
le.grid(row= 0, column= 4, padx = 10, pady = 5)
ee = ttk.Combobox(frame2, values= ["A: Reponer", "B: Reparar"])
ee.configure(state='readonly')
ee.grid(row= 1, column= 4, padx = 10, pady = 5)
lid = tk.Label(frame2, text= "ID:")
lid.grid(row= 6, column= 0)
eid = ttk.Entry(frame2)
eid.insert(0, str(pid))
e12.configure(state='readonly')
eid.grid(row= 6, column= 1, pady= 5)

# Treeview
headers = ("CANTIDAD", "REPUESTOS", "UNITARIO", "A/B", "TOTAL")
tree = ttk.Treeview(frame2, columns=headers, show="headings")
tree.heading("CANTIDAD", text="CANTIDAD")
tree.heading("REPUESTOS", text="REPUESTOS")
tree.heading("UNITARIO", text="UNITARIO")
tree.heading("A/B", text="A/B")
tree.heading("TOTAL", text="TOTAL")
tree.tag_configure("odd", background= "#F5F5F5")
tree.tag_configure("even", background= "#FFFFFF")
tree.grid (row = 2, columnspan = 6, rowspan = 4, pady = 10, padx = 10)
addb = ttk.Button(frame2, text = "Agregar", command = add_item)
addb.grid(row= 2, column= 6, padx = 10, pady = 10)
genb = ttk.Button(frame2, text= "Generar", command= gen_pres)
genb.grid(row= 3, column= 6, padx = 10, pady = 10)

# Frame-Packs
frame1.pack(side = "left", padx = 20, pady = 20)
frame2.pack(side = "right", padx = 20, pady = 20)

app.mainloop()