# ===========================================
#         LA POSADA - PERSISTENCIA
# ===========================================

# persistencia.py
# Encargado de guardar y cargar el estado del programa

# IMPORTACIONES
import json
import os

# ===========================================
#           FUNCIONES DE GESTION 
# ===========================================

import json
import os


def guardar_estado(estado: dict, archivo: str = 'datos.json') -> None:
    '''
    Guarda el estado completo del programa en un archivo JSON.
    '''
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(estado, f, indent=4, ensure_ascii=False)


def cargar_estado(archivo: str = 'datos.json') -> dict | None:
    '''
    Carga el estado del programa desde un archivo JSON.
    Devuelve None si el archivo no existe.
    '''
    if not os.path.exists(archivo):
        return None

    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)