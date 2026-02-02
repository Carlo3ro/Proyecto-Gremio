# ===========================================
#     LOGROS DEL GREMIO - ESTADISTICAS
# ===========================================

def registrar_items_raros(
    items_raros: list,
    evento: dict,
    reloj: dict,
    estado: dict
):
    '''
    Guarda en el historial de estadisticas los items
    raros obtenidos en una expedicion
    '''
    historial = estado['estadisticas']['items_raros_obtenidos']

    for item in items_raros:
        historial.append ({
            'item': item,
            'dia': reloj['dia'],
            'hora': reloj['hora'],
            'mazmorra': evento['mazmorra'],
            'dificultad': evento['dificultad'],
            'evento_id': evento['id']
        })
