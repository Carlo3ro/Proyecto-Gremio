# ===========================================
#    GUIA DE AVENTUREROS - RESTRICCIONES
# ===========================================

# restricciones.py
# Este modulo contiene los requisitos necesarios
# para comenzar una expedicion

# ===========================================
#         FUNCIONES DE VALIDACION
# ===========================================

def validar_codependencia(recursos_usados: dict):
    '''
    Valida si los aventureros tienen las armas
    necesarias
    '''
    aventureros_evento = recursos_usados['aventureros']
    armas_evento = recursos_usados['armas']

    requisitos = {
        'guerrero': ['Espada Larga', 'Escudo de Hierro'],
        'mago': ['Baculo Magico'],
        'sanador': ['Baculo Sanador'],
        'arquero': ['Arco de Roble'],
        'picaro': ['Dagas Dobles']
    }

    for aventurero, cantidad in aventureros_evento.items():
        if cantidad <= 0:
            continue

        if aventurero not in requisitos:
            return False, f'No hay requisitos definidos para {aventurero}'

        armas_necesarias = requisitos[aventurero]

        for arma in armas_necesarias:
            if arma not in armas_evento or armas_evento[arma] <= 0:
                return False, f'Falta {arma} para el {aventurero}'

    return True, 'Co-dependencia válida'

def validar_aventureros_unicos (aventureros_evento: dict):
    '''
    Verifica si no hay aventureros duplicados
    '''
    for aventurero, cantidad in aventureros_evento.items():
        if cantidad > 1:
            return False, f'No se permiten multiples {aventurero}s en el mismo evento'
    return True, 'Aventureros unicos validados'

def validar_compatibilidad_aventurero_arma(recursos_usados: dict):
    '''
    Valida si las armas seleccionadas puedes
    ser usadas por los aventureros
    '''
    aventureros_evento = recursos_usados['aventureros']
    armas_evento = recursos_usados['armas']

    compatibilidad = {
        'guerrero': ['Espada Larga', 'Escudo de Hierro'],
        'mago': ['Baculo Magico'],
        'sanador': ['Baculo Sanador'],
        'arquero': ['Arco de Roble'],
        'picaro': ['Dagas Dobles']
    }

    armas_seleccionadas = set()

    for aventurero, cantidad in aventureros_evento.items():
        if aventurero not in compatibilidad:
            return False, f'No hay requisitos definidos para: {aventurero}'
        if cantidad > 0 and aventurero in compatibilidad:
            armas_seleccionadas.update(compatibilidad[aventurero])

    for arma, cantidad in armas_evento.items():
        if cantidad > 0 and arma not in armas_seleccionadas:
            return False, f'El arma {arma} no es compatible con los aventureros seleccionados'

    return True, 'Compatibilidad aventurero-arma válida'

def validar_min_aventureros(dificultad: str, aventureros_evento: dict):
    requisitos_aventureros = {
        'C': 2,
        'B': 3,
        'A': 4,
        'S': 5
    }

    if dificultad not in requisitos_aventureros:
        return True, None 
    
    minimo = requisitos_aventureros[dificultad]
    cantidad = len(aventureros_evento)

    if cantidad < minimo:
        return False, f'La mazmorra de dificultad {dificultad} requiere al menos {minimo} aventureros'
    
    return True, None