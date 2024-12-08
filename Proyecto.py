import tkinter as tk
from tkinter import messagebox, ttk
import json

# Cargar datos de sensores desde el archivo JSON
def cargar_datos():
    with open("sensores.json", "r") as archivo:
        return json.load(archivo)

# Guardar datos en el archivo JSON
def guardar_datos():
    with open("sensores.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

datos = cargar_datos()

# Cambiar entre frames
def mostrar_frame(frame):
    frame.tkraise()

# Mostrar los sensores según la categoría seleccionada
def mostrar_rango():
    categoria = combo_categoria.get()
    if not categoria:
        messagebox.showerror("Error", "Por favor selecciona una categoría.")
        return
    sensores = datos["Sensores"][categoria]
    rangos = list(set(sensor["rango_trabajo"] for sensor in sensores))
    combo_rango["values"] = rangos
    combo_rango.set("")
    mostrar_frame(frame_rango)

def mostrar_marca():
    categoria = combo_categoria.get()
    rango = combo_rango.get()
    if not rango:
        messagebox.showerror("Error", "Por favor selecciona un rango.")
        return
    sensores = [
        sensor for sensor in datos["Sensores"][categoria]
        if sensor["rango_trabajo"] == rango
    ]
    marcas = list(set(sensor["marca"] for sensor in sensores))
    combo_marca["values"] = marcas
    combo_marca.set("")
    mostrar_frame(frame_marca)

def mostrar_modelo():
    categoria = combo_categoria.get()
    rango = combo_rango.get()
    marca = combo_marca.get()
    if not marca:
        messagebox.showerror("Error", "Por favor selecciona una marca.")
        return
    sensores = [
        sensor for sensor in datos["Sensores"][categoria]
        if sensor["rango_trabajo"] == rango and sensor["marca"] == marca
    ]
    modelos = [sensor["modelo"] for sensor in sensores]
    combo_modelo["values"] = modelos
    combo_modelo.set("")
    mostrar_frame(frame_modelo)

def mostrar_resultado():
    categoria = combo_categoria.get()
    modelo = combo_modelo.get()
    if not modelo:
        messagebox.showerror("Error", "Por favor selecciona un modelo.")
        return
    sensor = next(
        sensor for sensor in datos["Sensores"][categoria] if sensor["modelo"] == modelo
    )
    resultado = (
        f"Sensor seleccionado:\n\n"
        f"Nombre: {sensor['nombre']}\n"
        f"Modelo: {sensor['modelo']}\n"
        f"Marca: {sensor['marca']}\n"
        f"Rango de Trabajo: {sensor['rango_trabajo']}\n\n"
        f"Descripción:\n{sensor['descripcion']}"
    )
    lbl_resultado.config(text=resultado)
    mostrar_frame(frame_resultado)

# Agregar un nuevo sensor al sistema
def agregar_sensor():
    categoria = entry_categoria.get()
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    modelo = entry_modelo.get()
    marca = entry_marca.get()
    rango = entry_rango.get()
    descripcion = text_descripcion.get("1.0", "end-1c")
    
    if not all([categoria, codigo, nombre, modelo, marca, rango, descripcion]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if categoria not in datos["Sensores"]:
        datos["Sensores"][categoria] = []

    nuevo_sensor = {
        "codigo": codigo,
        "nombre": nombre,
        "modelo": modelo,
        "marca": marca,
        "rango_trabajo": rango,
        "descripcion": descripcion
    }
    datos["Sensores"][categoria].append(nuevo_sensor)
    guardar_datos()
    messagebox.showinfo("Éxito", "El sensor ha sido agregado exitosamente.")
    mostrar_frame(frame_categoria)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema Experto de Sensores")
root.geometry("500x600")

# Crear frames
frame_categoria = tk.Frame(root)
frame_rango = tk.Frame(root)
frame_marca = tk.Frame(root)
frame_modelo = tk.Frame(root)
frame_resultado = tk.Frame(root)
frame_agregar = tk.Frame(root)

for frame in (frame_categoria, frame_rango, frame_marca, frame_modelo, frame_resultado, frame_agregar):
    frame.grid(row=0, column=0, sticky="nsew")

# Frame Categoría
tk.Label(frame_categoria, text="Selecciona una categoría:").pack(pady=10)
categorias = list(datos["Sensores"].keys())
combo_categoria = ttk.Combobox(frame_categoria, values=categorias, state="readonly")
combo_categoria.pack(pady=10)
tk.Button(frame_categoria, text="Siguiente", command=mostrar_rango).pack(pady=10)
tk.Button(frame_categoria, text="Agregar Nuevo Sensor", command=lambda: mostrar_frame(frame_agregar)).pack(pady=10)

# Frame Rango
tk.Label(frame_rango, text="Selecciona un rango:").pack(pady=10)
combo_rango = ttk.Combobox(frame_rango, state="readonly")
combo_rango.pack(pady=10)
tk.Button(frame_rango, text="Siguiente", command=mostrar_marca).pack(pady=10)
tk.Button(frame_rango, text="Atrás", command=lambda: mostrar_frame(frame_categoria)).pack(pady=10)

# Frame Marca
tk.Label(frame_marca, text="Selecciona una marca:").pack(pady=10)
combo_marca = ttk.Combobox(frame_marca, state="readonly")
combo_marca.pack(pady=10)
tk.Button(frame_marca, text="Siguiente", command=mostrar_modelo).pack(pady=10)
tk.Button(frame_marca, text="Atrás", command=lambda: mostrar_frame(frame_rango)).pack(pady=10)

# Frame Modelo
tk.Label(frame_modelo, text="Selecciona un modelo:").pack(pady=10)
combo_modelo = ttk.Combobox(frame_modelo, state="readonly")
combo_modelo.pack(pady=10)
tk.Button(frame_modelo, text="Siguiente", command=mostrar_resultado).pack(pady=10)
tk.Button(frame_modelo, text="Atrás", command=lambda: mostrar_frame(frame_marca)).pack(pady=10)

# Frame Resultado
lbl_resultado = tk.Label(frame_resultado, text="", wraplength=400, justify="left")
lbl_resultado.pack(pady=20)
tk.Button(frame_resultado, text="Inicio", command=lambda: mostrar_frame(frame_categoria)).pack(pady=10)

# Frame Agregar Sensor
tk.Label(frame_agregar, text="Categoría:").pack(pady=5)
entry_categoria = tk.Entry(frame_agregar)
entry_categoria.pack(pady=5)

tk.Label(frame_agregar, text="Código:").pack(pady=5)
entry_codigo = tk.Entry(frame_agregar)
entry_codigo.pack(pady=5)

tk.Label(frame_agregar, text="Nombre:").pack(pady=5)
entry_nombre = tk.Entry(frame_agregar)
entry_nombre.pack(pady=5)

tk.Label(frame_agregar, text="Modelo:").pack(pady=5)
entry_modelo = tk.Entry(frame_agregar)
entry_modelo.pack(pady=5)

tk.Label(frame_agregar, text="Marca:").pack(pady=5)
entry_marca = tk.Entry(frame_agregar)
entry_marca.pack(pady=5)

tk.Label(frame_agregar, text="Rango de Trabajo:").pack(pady=5)
entry_rango = tk.Entry(frame_agregar)
entry_rango.pack(pady=5)

tk.Label(frame_agregar, text="Descripción:").pack(pady=5)
text_descripcion = tk.Text(frame_agregar, height=5, width=40)
text_descripcion.pack(pady=5)

tk.Button(frame_agregar, text="Guardar", command=agregar_sensor).pack(pady=10)
tk.Button(frame_agregar, text="Cancelar", command=lambda: mostrar_frame(frame_categoria)).pack(pady=10)

# Mostrar la primera pantalla
mostrar_frame(frame_categoria)
root.mainloop()
