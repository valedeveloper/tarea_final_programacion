import tkinter as tk
from tkinter import messagebox
from tkinter import font
import random
import math
import csv
import os 
from logica import Recetario

base = tk.Tk()
base.resizable(False, False)

base.title("Gestor de Recetas")

recetario = Recetario()

#Funciones botones
def agregar_receta():
    nombre = entry_nombre.get().strip()
    temperatura_str = entry_temperatura.get()
    if not nombre or not temperatura_str:
        messagebox.showinfo("Atención","Ingresa nombre y temperatura")
        return
    try:
        celsius = int(temperatura_str)
    except ValueError:
        messagebox.showinfo("Atención","Temperatura debe ser un número")
        return
    
    text_area.delete("1.0", "end")         
    recetario.agregar_receta(nombre, celsius)
    messagebox.showinfo("Atención","Receta añadida")
    
    df_recetas = recetario.mostrar_recetas()  
    text_area.insert(tk.END, df_recetas.to_string(index=False))  
    
    entry_nombre.delete(0, tk.END)
    entry_temperatura.delete(0, tk.END)

def eliminar_receta():
    try:
        id_objetivo = int(entry_numero.get())
        receta_eliminada = recetario.eliminar_receta_por_id(id_objetivo)
        if receta_eliminada:
            text_area.delete("1.0", "end") 
            messagebox.showinfo("Atención","Receta Eliminada")
            df_recetas = recetario.mostrar_recetas()  
            text_area.insert(tk.END, df_recetas.to_string(index=False)) 
            entry_numero.delete("1.0", "end") 
            # text_area.insert(tk.END, f"Receta eliminada:\n")
        else:
            messagebox.showinfo("Atención",f"No se encontró una receta con el ID {id_objetivo}")
    except ValueError:
        messagebox.showinfo("Atención","Ingresa un número de ID válido")

def actualizar_archivo():
    text_area.delete("1.0", "end") 
    df_recetas=recetario.actualizar_archivo()
    if not df_recetas.empty :
        texto_tabla = df_recetas.to_string(index=False)
        columnas_recetas = df_recetas.columns
        encabezado = "  ".join([str(col).upper() for col in columnas_recetas])
        text_area.insert(tk.END, f"{encabezado}\n")
        text_area.insert(tk.END, texto_tabla)
    else:
        text_area.insert(tk.END, "No hay recetas registradas.")

def ver_receta_por_nombre():
    nombre = entry_busqueda_nombre.get().strip()
    if not nombre:
        messagebox.showinfo("Ingresa un nombre para buscar.")
        return
    resultados = recetario.buscar_por_nombre(nombre)
    print("Los resuktaso", resultados)
    text_area.delete("1.0", "end")
    if not resultados.empty:
        text_area.insert(tk.END, resultados.to_string(index=False))
    else:
        text_area.insert(tk.END, "Atención","No se encontraron recetas con ese nombre.")
    entry_busqueda_nombre.delete(0, tk.END)
   

#Entradas
# Fuente en negrita para los headers
negrita = font.Font(weight="bold")

#Nombre y Temperatura
tk.Label(base, text="Nombre de la receta:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(base)
entry_nombre.grid(row=0, column=1, padx=5)

tk.Label(base, text="Temperatura (°C):").grid(row=0, column=2, padx=5, pady=5)
entry_temperatura = tk.Entry(base)
entry_temperatura.grid(row=0, column=3, padx=5)

# Botones: Registrar y Guardar
tk.Button(base, text="Registrar Receta", bg="#90EE90", command=agregar_receta).grid(row=0, column=4, padx=5, pady=5)
tk.Button(base, text="Guardar/Actualizar Archivo", bg="#ADD8E6", command=actualizar_archivo).grid(row=0, column=5, padx=5, pady=5)

# Botones: Eliminar receta por número
tk.Label(base, text="Número de receta:").grid(row=1, column=0, padx=5, pady=5)
entry_numero = tk.Entry(base)
entry_numero.grid(row=1, column=1, padx=5)

tk.Button(base, text="Eliminar Receta", bg="#FF7F7F", command=eliminar_receta).grid(row=1, column=2, padx=5, pady=5)

# Buscar por nombre
tk.Label(base, text="Buscar receta por nombre:").grid(row=2, column=0, padx=5, pady=5)
entry_busqueda_nombre = tk.Entry(base)
entry_busqueda_nombre.grid(row=2, column=1, padx=5, pady=5)
tk.Button(base, text="Buscar", bg="#6ECFFF", command=ver_receta_por_nombre).grid(row=2, column=2, padx=5, pady=5)

# Mostrar recetas
text_area = tk.Text(base, width=80, height=20)
text_area.grid(row=3, column=0, columnspan=6, padx=10, pady=10)
text_area.grid_propagate(False)

# Mostrar recetas automáticamente al cargar
df_recetas = recetario.mostrar_recetas()
if not df_recetas.empty :
    texto_tabla = df_recetas.to_string(index=False)
    columnas_recetas = df_recetas.columns
    # encabezado = "  ".join([str(col).upper() for col in columnas_recetas])
    # text_area.insert(tk.END, f"{encabezado}\n")
    text_area.insert(tk.END, texto_tabla)
else:
    text_area.insert(tk.END, "No hay recetas registradas.")

base.mainloop()