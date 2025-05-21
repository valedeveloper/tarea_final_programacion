
import csv
import os
import random
import pandas as pd

class Recetario:
    def __init__(self, archivo='recetas.csv'):
        self.archivo = archivo
        self.campos = ['nombre', 'tiempo_coccion_min', 'temperatura_farenheit']
        # self._asegurar_archivo()

    def _convertir_a_fahrenheit(self, celsius):
        return (celsius * 1.8) + 32
    
   
    def agregar_receta(self, nombre,celsius):
        """Agrega una receta con tiempo random y temperatura  a Fahrenheit."""
        tiempo_coccion = random.randint(15, 90)
        temperatura_farenheit = self._convertir_a_fahrenheit(celsius)
        receta = {
            'nombre': nombre,
            'tiempo_coccion_min': tiempo_coccion,
            'temperatura_farenheit': round(temperatura_farenheit, 2)
        }

        with open(self.archivo, 'a', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos)
            if not self.archivo:
                escritor.writeheader()
            escritor.writerow(receta)
        return receta   
    
    def mostrar_receta(self):
        """Mostrar recetas del archivo"""
        if os.path.isfile(self.archivo):
            df = pd.read_csv(self.archivo)
            print(df)
            return df
        else:
            print("No hay registros disponibles.")
            return pd.DataFrame(columns=self.campos)
        
        
    def ver_receta_especifico(self, id):
        """Devuelve una receta por su número (índice)."""
        recetas = self.mostrar_receta()
        if 0 <= id < len(recetas):
            return recetas[id]
        else:
            print("Id fuera del rango")

    def eliminar_receta_especifico(self, numero):
            """Elimina una receta por su número (índice)."""
            recetas = self.mostrar_receta()
            if 0 <= numero < len(recetas):
                receta_eliminada = recetas.pop(numero)
                with open(self.archivo, 'a', newline='') as f:
                    escritor = csv.DictWriter(f, fieldnames=self.campos)
                    if not self.archivo:
                        escritor.writeheader()
                    escritor.writerow(recetas)
                return receta_eliminada   
            else:
                print("No hay registros disponibles en esta receta")
                return None


   
    # def _asegurar_archivo(self):
    #     """Crea el archivo si no existe."""
    #     if not os.path.exists(self.archivo):
    #         with open(self.archivo, 'w', newline='', encoding='utf-8') as f:
    #             writer = csv.DictWriter(f, fieldnames=self.campos)
    #             writer.writeheader()
    #         # with open(archivo_csv, 'a', newline='') as f:
    #         #     escritor = csv.DictWriter(f, fieldnames=fila.keys())
    #         #     if not archivo_existe:
    #         #         escritor.writeheader()
    #         #     escritor.writerow(fila)


    def actualizar_archivo(self, recetas):
        """Sobrescribe el archivo con una nueva lista de recetas."""
        with open(self.archivo, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.campos)
            writer.writeheader()
            writer.writerows(recetas)

    



recetario = Recetario()



recetario.agregar_receta("Receta 1", 30)
recetario.mostrar_receta()

