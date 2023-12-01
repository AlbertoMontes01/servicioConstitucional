import tkinter as tk
from tkinter import filedialog
import re

class Nodo:
    def __init__(self, palabra):
        self.palabra = palabra
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, palabra):
        if self.raiz is None:
            self.raiz = Nodo(palabra)
        else:
            self._insertar_recursivo(palabra, self.raiz)

    def _insertar_recursivo(self, palabra, nodo_actual):
        if palabra < nodo_actual.palabra:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(palabra)
            else:
                self._insertar_recursivo(palabra, nodo_actual.izquierda)
        elif palabra > nodo_actual.palabra:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(palabra)
            else:
                self._insertar_recursivo(palabra, nodo_actual.derecha)

    def imprimir_inorden(self, nodo_actual):
        if nodo_actual:
            self.imprimir_inorden(nodo_actual.izquierda)
            print(nodo_actual.palabra)
            self.imprimir_inorden(nodo_actual.derecha)

def limpiar_palabra(palabra):
    # Eliminar acentos y convertir a minúsculas
    palabra = palabra.lower().encode('ascii', 'ignore').decode('utf-8')
    # Eliminar caracteres especiales y números
    palabra = re.sub(r'[^a-zA-Z]', '', palabra)
    return palabra

def eliminar_numeros_romanos(texto):
    # Patrón para identificar números romanos
    patron_romano = re.compile(r'\b(?:[IVXLCDM]+|\d+)\b')
    # Reemplazar números romanos con una cadena vacía
    texto_limpio = patron_romano.sub('', texto)
    return texto_limpio

def limpiar_texto(texto):
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_limpias = [limpiar_palabra(palabra) for palabra in palabras]
    return palabras_limpias

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    # Seleccionar archivo usando el diálogo de selección de archivos
    archivo_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Archivos PDF", "*.pdf")])

    root.destroy()  # Cerrar la ventana de Tkinter

    return archivo_path

# Procesar el archivo seleccionado
ruta_archivo = seleccionar_archivo()
if ruta_archivo:
    with open(ruta_archivo, 'r', encoding='utf-8') as txt_file:
        contenido = txt_file.read()
        contenido_limpiado = eliminar_numeros_romanos(contenido)
        palabras_limpias = limpiar_texto(contenido_limpiado)

        arbol = ArbolBinario()
        for palabra in palabras_limpias:
            arbol.insertar(palabra)

        print("Árbol de Palabras Binarias:")
        arbol.imprimir_inorden(arbol.raiz)

