import tkinter as tk
import ttkbootstrap as ttk
import datetime, os, sqlite3, csv
from docxtpl import DocxTemplate
from docx2pdf import convert
from tkinter import messagebox, filedialog, Toplevel
from ttkwidgets.autocomplete import *
from pathlib import Path
from ddbb import nventana
from filetree import abrir
from ttkbootstrap.constants import *

# DDBB Conx
conn = sqlite3.connect('./files/presdb.db')
cur = conn.cursor()

def query() :
    values = ('''INSERT INTO clientes (pres_id, nombre, apellido, path, fecha)
                VALUES (?, ?, ?, ?, ?)''')
    d_tuple = (pid, e1.get().upper(), e2.get().upper(), doc_path.replace(".docx",".pdf"), t.strftime("%d/%m/%Y"))
    cur.execute(values, d_tuple)
    conn.commit()

# SystemConfig
app = tk.Tk()
app.title ("PresGen V1.0")
app.resizable (False, False)
style = ttk.Style ("flatly")
app.config (bg="grey")

# Varibles / Lists / Misc
idfile = Path("./files/id.txt")
savefile = './files/savepath.txt'
t = datetime.datetime.now()
pid = 0
repuestos = []
pres_list = []
caps = tk.StringVar()

def caps(event) :
    caps.set(caps.get().upper())

with open("./files/repuestos.csv", encoding='utf-8', errors='ignore') as csv_file:
    next(csv_file)
    for line in csv_file:
        data = line.strip().split(',')
        if len(data) == 1:  
            repuestos.append(data[0])  # Agregar el nombre del repuesto

if os.path.exists(idfile):
    with open(idfile, "r", encoding="utf-8") as f:
        content = f.read().strip()
        pid = int(content) if content.isdigit() else 0
else: 
    with open(idfile, "w", encoding="utf-8") as f:
        f.write('0')
        pid = 0

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
    global cantidad, repuestos, unitario, ab, precio
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

def del_item() :
    focus_item = tree.focus()
    if not focus_item : 
        messagebox.showwarning("AVISO!", "No hay ningun item seleccionado")
        return

    item_values = tree.item(focus_item, 'values')
    try :
        cantidad = int(item_values[0])
        repuesto = item_values[1]
        unitario = float(item_values[2])
        estado = item_values[3]
        total = float(item_values[4])

        pres_list.remove([cantidad, repuesto, unitario, estado, total])
    
        tree.delete(focus_item)

    except ValueError:
        pass
    except Exception as e:
         messagebox.showerror("Error", f"Ocurrió un error al eliminar el ítem: {e}")

def upd_ventana() :
    focus_item = tree.focus()
    if not focus_item : 
        messagebox.showwarning("AVISO!", "No hay ningun item seleccionado")
        return
    
    item_values = tree.item(focus_item, 'values')
    try :
        ncantidad = int(item_values[0])
        nrepuesto = item_values[1]
        nunitario = float(item_values[2])
        nestado = item_values[3]
        total = float(item_values[4])

        ventana = Toplevel()
        ventana.title("Modificar Item")
        ventana.config(width= 300, height= 200, bg= "grey")
        nframe = ttk.Frame(ventana, width= 100, height= 100, borderwidth = 1, relief = "solid")

        nl1 = ttk.Label(nframe, text= "Cantidad:")
        nl2 = ttk.Label(nframe, text= "Repuesto:")
        nl3 = ttk.Label(nframe, text= "Unitario:")
        nl4 = ttk.Label(nframe, text= "Estado:")
        nl1.grid(row= 0, column= 0, padx = 10, pady = 10)
        nl2.grid(row= 0, column= 1, padx = 10, pady = 10)
        nl3.grid(row= 2, column= 0, padx = 10, pady = 10)
        nl4.grid(row= 2, column= 1, padx = 10, pady = 10)

        ne1 = ttk.Entry(nframe)
        ne1.insert(0,ncantidad)
        ne2 = AutocompleteCombobox(nframe, completevalues=repuestos, width= 30)
        ne2.insert(0,nrepuesto)
        ne3 = ttk.Entry(nframe)
        ne3.insert(0,nunitario)
        ne4 = ttk.Combobox(nframe, values= ["A: Reponer", "B: Reparar"], bootstyle= "dark")
        ne4.insert(0,nestado)

        ne1.grid(row= 1, column= 0, padx = 10, pady = 10)
        ne2.grid(row= 1, column= 1, padx = 10, pady = 10)
        ne3.grid(row= 3, column= 0, padx = 10, pady = 10)
        ne4.grid(row= 3, column= 1, padx = 10, pady = 10)

        def upd_item() :
                new1 = int(ne1.get())
                new2 = ne2.get()
                new3 = float(ne3.get())
                new4 = ne4.get()
                new5 = new1 * new3
                if not new1 or not new2 or not new3 or not new4 :
                    messagebox.showerror("Error", "Todos los campos son obligartorios")
                    return
                original_values = tree.item(focus_item, 'values')
                ocantidad = int(original_values[0])
                orepuesto = original_values[1]
                ounitario = float(original_values[2])
                oestado = original_values[3]
                ototal = float(original_values[4])
                
                # Reemplazar el ítem en la lista
                for idx, item in enumerate(pres_list):
                    if (
                        item[0] == ocantidad and
                        item[1] == orepuesto and
                        item[2] == ounitario and
                        item[3] == oestado and
                        item[4] == ototal
                    ):
                        pres_list[idx] = [new1, new2, new3, new4, new5]
                        break

                # Actualizamos el treeview
                tree.item(focus_item, values=(new1, new2, new3, new4, new5))
                messagebox.showinfo("Aviso", "Ítem modificado correctamente!")
                ventana.destroy()

    except ValueError as e:
        messagebox.showerror("Error", f"Error de conversión: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

    nb = ttk.Button(nframe, text= "Modificar", command= upd_item)
    nb.grid(row= 4, column= 0, columnspan= 2, padx= 10, pady= 10)

    nframe.grid(column= 0, row= 0, padx= 20, pady= 20)

def load_csv():
    def callback_csv(ruta_archivo):
        if ruta_archivo.endswith('.csv'):
            try:
                for i in tree.get_children():
                    tree.delete(i)
                pres_list.clear()

                with open(ruta_archivo, newline='', encoding='utf-8') as myfile:
                    csvread = csv.reader(myfile, delimiter=',')
                    entry_loaded = False
                    rows = list(csvread)

                    for row in rows:
                        if not row:
                            continue  # Saltar filas vacías

                        if row[0].strip().upper() == "ENTRYDATA":
                            # Lista de entries en el mismo orden que los datos
                            entry_widgets = [e1, e3, e4, e5, e6, e7, e8, e9, e10]

                            for i, entry in enumerate(entry_widgets, start=1):
                                entry.delete(0, tk.END)
                                if i < len(row) and row[i].strip():
                                    entry.insert(0, row[i])
                            entry_loaded = True
                        else:
                            if len(row) < 1 or row[0].strip().upper() == "ENTRYDATA":
                                continue  # saltar entrada incompleta o mal formateada

                            # Rellenar con valores por defecto si faltan columnas
                            while len(row) < 5:
                                row.append('')

                            try:
                                cant = int(row[0]) if row[0] else 0
                                rep = row[1] if row[1] else ''
                                punit = float(row[2]) if row[2] else 0.0
                                cat = row[3] if row[3] else ''
                                total = float(row[4]) if row[4] else 0.0

                                tree.insert("", 'end', values=[cant, rep, punit, cat, total])
                                pres_list.append([cant, rep, punit, cat, total])
                            except ValueError:
                                print(f"Fila inválida (omitida): {row}")

                if not entry_loaded:
                    print("No se encontró línea ENTRYDATA")
            except Exception as e:
                messagebox.showerror("Error al leer archivo", f"{e}")
        else:
            messagebox.showerror("El archivo seleccionado no es un CSV")

    abrir(callback_csv)

def save_csv():
    def guardar_ruta_savefile(path):
        with open(savefile, 'w', encoding='utf-8') as f:
            f.write(path)

    def cargar_ruta_savefile():
        if os.path.exists(savefile):
            with open(savefile, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return None

    def seleccionar_o_cargar_ruta():
            ruta_guardada = cargar_ruta_savefile()
            if ruta_guardada and os.path.isdir(ruta_guardada):
                return ruta_guardada
            else:
                path = filedialog.askdirectory(title="Seleccionar carpeta principal")
                if path:
                    guardar_ruta_savefile(path)
                    return path
                else:
                    return

    try: 
        # sf = filedialog.asksaveasfilename(initialfile=f"Suspenso_{e2.get().upper()}", defaultextension=".csv", filetypes=[("CommaSeparatedFile", "*.csv")])
        sf_r = seleccionar_o_cargar_ruta()
        sf_c = os.path.join(sf_r , f"Suspenso-{e2.get().upper()}" + ".csv")
        sf = open(sf_c, "w")
        if not sf:
            return
        
        with open(sf_c, "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')

            csvwriter.writerow([
                e1.get(), e2.get(), e3.get(), e4.get(), e5.get(),
                e6.get(), e7.get(), e8.get(), e9.get(), e10.get()
            ])

            # Guardar datos de Entry al principio
            entry_row = [
                "ENTRYDATA",
                e1.get(),  # nombre
                e3.get(),  # domicilio
                e4.get(),  # teléfono
                e5.get(),  # vehículo
                e6.get(),  # marca
                e7.get(),  # modelo
                e8.get(),  # motor
                e9.get(),  # chasis
                e10.get()  # dominio
            ]
            csvwriter.writerow(entry_row)

            for row_id in tree.get_children():
                row = tree.item(row_id)['values']
                print('save row:', row)
                csvwriter.writerow(row)
                tree.delete(*tree.get_children())
                messagebox.showinfo ("Aviso!", "Archivo Guardado correctamente!")

    except Exception as e:
        messagebox.showerror ("Aviso!", f"No se guardo el archivo: {e}")

def abrir_pdf(pdf_path):
    abs_path = os.path.abspath(pdf_path)
    if os.path.exists(abs_path):
        os.startfile(abs_path)  # Esto abre el PDF con Edge o el visor predeterminado
    else:
        messagebox.showerror("Error", "El archivo PDF no existe.")

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
    dc = doc_path
    os.remove(doc_path)
    messagebox.showinfo("Aviso!", "Presupuesto Generado!")

    abrir_pdf(dc.replace(".docx", ".pdf"))
    
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
e1 = ttk.Entry(frame1, textvariable= caps, bootstyle= "dark")
e2 = ttk.Entry(frame1, textvariable= caps, bootstyle= "dark")
e3 = ttk.Entry(frame1, textvariable= caps, bootstyle= "dark")
e4 = ttk.Entry(frame1, bootstyle= "dark")
e5 = ttk.Entry(frame1, textvariable= caps, bootstyle= "dark")
e6 = ttk.Entry(frame1, textvariable= caps, bootstyle= "dark")
e7 = ttk.Entry(frame1, bootstyle= "dark")
e8 = ttk.Entry(frame1, bootstyle= "dark")
e9 = ttk.Entry(frame1, bootstyle= "dark")
e10 = ttk.Entry(frame1, textvariable= caps, bootstyle= "dark")
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
e11 = ttk.Entry(frame2, bootstyle= "dark")
e12 = AutocompleteCombobox (frame2, width= 35, completevalues=repuestos, bootstyle= "dark")
e12.configure(state='normal')
e11.grid(row= 1, column= 1, padx = 10, pady = 5)
e12.grid(row= 1, column= 2, padx = 10, pady = 5)

ep = ttk.Entry(frame2, bootstyle= "dark")
ep.grid(row= 1, column= 3, padx = 10, pady = 5)
le = tk.Label(frame2, text="Estado:")
le.grid(row= 0, column= 4, padx = 10, pady = 5)
ee = ttk.Combobox(frame2, values= ["A: Reponer", "B: Reparar"], bootstyle= "dark")
ee.configure(state='readonly')
ee.grid(row= 1, column= 4, padx = 10, pady = 5)
lid = tk.Label(frame2, text= "ID:")
lid.grid(row= 6, column= 0)
eid = ttk.Entry(frame2, state= "normal", bootstyle= "dark")
eid.insert(0, str(pid))
eid.grid(row= 6, column= 1, pady= 5)

# Treeview
headers = ("CANTIDAD", "REPUESTOS", "UNITARIO", "A/B", "TOTAL")
tree = ttk.Treeview(frame2, columns=headers, show="headings", bootstyle= "dark")
tree.heading("CANTIDAD", text="CANTIDAD")
tree.column("CANTIDAD", anchor="center")
tree.heading("REPUESTOS", text="REPUESTOS")
tree.column("REPUESTOS", anchor="center")
tree.heading("UNITARIO", text="UNITARIO")
tree.column("UNITARIO", anchor="center")
tree.heading("A/B", text="A/B")
tree.column("A/B", anchor="center")
tree.heading("TOTAL", text="TOTAL")
tree.column("TOTAL", anchor="center")
tree.tag_configure("odd", background= "grey", foreground= "white")
tree.tag_configure("even", background= "white", foreground= "black")
tree.grid (row = 2, columnspan = 6, rowspan = 4, pady = 10, padx = 10)
addb = ttk.Button(frame2, text = "Agregar", command = add_item)
addb.grid(row= 2, column= 6, padx = 10, pady = 10)
modb = ttk.Button(frame2, text = "Modificar", command = upd_ventana, bootstyle= "warning")
modb.grid(row= 3, column= 6, padx = 10, pady = 10)
delb = ttk.Button(frame2, text= "Eliminar", command= del_item, bootstyle= "danger")
delb.grid(row= 4, column= 6, padx= 10, pady= 10)
genb = ttk.Button(frame2, text= "Generar", command= gen_pres, bootstyle= "success")
genb.grid(row= 5, column= 6, padx = 10, pady = 10)
#####
saveb = ttk.Button(frame2, text= "Guardar Presupuesto", command= save_csv, bootstyle= "secondary")
saveb.grid(row= 6, column= 3, padx = 10, pady = 10)
openb = ttk.Button(frame2, text= "Abrir Presupuesto", command= load_csv, bootstyle= "secondary")
openb.grid(row= 6, column= 4, padx = 10, pady = 10)
modib = ttk.Button(frame2, text= "Agregar Repuestos", command=lambda:os.system('python ./bin/mod.py'), bootstyle= "secondary")
modib.grid(row= 6, column= 2, padx = 10, pady = 10)

# Frame-Packs
frame1.pack(side = "left", padx = 20, pady = 20)
frame2.pack(side = "right", padx = 20, pady = 20)

if app.destroy == True :
    cur.close()

app.mainloop()