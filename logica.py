
import csv
import os
import random
import pandas as pd

class Recetario:
    def __init__(self, archivo='recetas.csv'):
        self.archivo = archivo
        self.campos = ['id','nombre', 'tiempo_coccion_min', 'temperatura_farenheit']
        self.id=1
      
    def _convertir_a_fahrenheit(self, celsius):
        """Convierte de Cellsius a Farneheit"""
        return (celsius * 1.8) + 32
    
    def agregar_receta(self, nombre, celsius):
        """Agrega una receta con tiempo random y temperatura en Fahrenheit."""
        tiempo_coccion = random.randint(15, 90)
        temperatura_farenheit = self._convertir_a_fahrenheit(celsius)
        
        receta = {
            'id': self.id,
            'nombre': nombre,
            'tiempo_coccion_min': tiempo_coccion,
            'temperatura_farenheit': round(temperatura_farenheit, 2)
        }

        archivo_existe = os.path.isfile(self.archivo)
        escribir_header = not archivo_existe or os.path.getsize(self.archivo) == 0

        with open(self.archivo, 'a', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos)
            if escribir_header:
                escritor.writeheader()
            escritor.writerow(receta)
        self.id += 1
        print(receta)
        return receta
    

    def mostrar_recetas(self):
        """Mostrar recetas del archivo"""
        if os.path.isfile(self.archivo):
            df = pd.read_csv(self.archivo)
            print("Desde mostrar",df)
            return df
        else:
            print("No hay registros disponibles.")
            return pd.DataFrame(columns=self.campos)
        
    def ver_receta_especifico(self, id):
        """Devuelve una receta por su número (id)."""
        recetas = self.mostrar_recetas()
        resultado = recetas[recetas['id'] == id]
        print(resultado,"Es errado")
        if not resultado.empty:
            receta = resultado.iloc[0]  
            print("La receta en específico:", receta)
            return receta
        else:
            print("ID no existe.")
            return None
        
    def eliminar_receta_por_id(self, id_eliminar):
        recetas = self.mostrar_recetas()
        if id_eliminar in recetas['id'].values:
            recetas = recetas[recetas['id'] != id_eliminar]  
            recetas.to_csv(self.archivo, index=False) 
            print(f"Receta con id {id_eliminar} eliminada.")
            return True
        else:
            print("Id no existe.")
            return False

    def actualizar_archivo(self):
        """Sobrescribe el archivo con una nueva lista de recetas."""
        archivo_existe = os.path.isfile(self.archivo)
        escribir_header = not archivo_existe or os.path.getsize(self.archivo) == 0
        recetas = self.mostrar_recetas()

        with open(self.archivo, 'a', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos)
            
            if escribir_header:
                escritor.writeheader()
            
            for _, fila in recetas.iterrows():
                escritor.writerow(fila.to_dict())
        return recetas

 