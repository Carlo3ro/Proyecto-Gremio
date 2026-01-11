# ===========================================
#      ALMACEN DEL GREMIO - RECURSOS
# ===========================================

# recursos.py
# Este modulo contiene la base de datos de recursos del gremio:
# aventureros, armas y mazmorras disponibles.

# IMPORTACIONES
import json
import os

# ===========================================
#          FUNCIONES DE GESTION 
# ===========================================

def guardar_estado(ruta: str, recursos: dict, eventos_activos: dict, historial: dict, reloj: dict):
    datos = {
        'recursos': recursos,
        'eventos_activos': eventos_activos,
        'historial': historial,
        'reloj': reloj
    }

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_estado(ruta: str):
    if not os.path.exists(ruta):
        return None

    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)