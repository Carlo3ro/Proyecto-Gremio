# ===========================================
#    GESTOR DE RECOMPENSAS - RECOMPENSAS
# ===========================================

# IMPORTACIONES
import random

# ===========================================
#     TABLAS DE RECOMPENSAS / ITEMS RAROS
# ===========================================

items_raros = {
    'Artefacto antiguo',
    'Pergamino raro',
    'Runa mágica',
}

recompensas_por_dificultad = {
    'F': {
        'oro': (10, 20),
        'objetos': [
            ('Poción pequeña', 0.40),
        ]
    },
    'D': {
        'oro': (20, 40),
        'objetos': [
            ('Poción pequeña', 0.50),
            ('Poción mediana', 0.20),
        ]
    },
    'C': {
        'oro': (40, 70),
        'objetos': [
            ('Poción mediana', 0.40),
            ('Pergamino', 0.15),
        ]
    },
    'B': {
        'oro': (70, 120),
        'objetos': [
            ('Poción grande', 0.35),
            ('Pergamino raro', 0.20),
        ]
    },
    'A': {
        'oro': (120, 200),
        'objetos': [
            ('Pergamino raro', 0.35),
            ('Artefacto antiguo', 0.10),
        ]
    },
    'S': {
        'oro': (250, 400),
        'objetos': [
            ('Artefacto antiguo', 0.40),
            ('Runa mágica', 0.10),
        ]
    }
}

# ===========================================
#          FUNCIONES DE GENERACION
# ===========================================

def generar_recompensas(dificultad: str, bonus_rareza: float = 1.0) -> dict:

    recompensas = {}

    if dificultad not in recompensas_por_dificultad:
        return recompensas

    data = recompensas_por_dificultad[dificultad]

    # Oro (siempre)
    oro_min, oro_max = data['oro']
    recompensas['Oro'] = random.randint(oro_min, oro_max)

    # Objetos aleatorios (con bonus)
    for nombre, prob in data['objetos']:
        prob_final = min(prob * bonus_rareza, 1.0)

        if random.random() <= prob_final:
            recompensas[nombre] = recompensas.get(nombre, 0) + 1

    return recompensas

def obtener_items_raros(recompensas: dict):
    return [item for item in recompensas if item in items_raros]