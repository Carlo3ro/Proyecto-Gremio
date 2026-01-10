# ===========================================
#    GUIA DE AVENTUREROS - RESTRICCIONES
# ===========================================

# restricciones.py
# Este modulo contiene los requisitos necesarios
# para comenzar una expedicion

# ===========================================
#          FUNCIONES DE GESTION 
# ===========================================

def validar_codependencia(aventureros_evento: dict, armas_evento: dict):
    '''
    Docstring for validar_codependencia
    '''
    requisitos = {
        'guerrero': ['Espada Larga', 'Escudo de Hierro'],
        'mago': ['Báculo Arcano'],
        'sanador': ['Báculo Sanador'],
        'arquero': ['Arco de Roble'],
        'picaro': ['Dagas Dobles']
    }

    for aventurero, cantidad in aventureros_evento.items():
        if cantidad <= 0:
            continue

        if aventurero not in requisitos:
            continue

        armas_necesarias = requisitos[aventurero]

        for arma in armas_necesarias:
            if arma not in armas_evento or armas_evento[arma] <= 0:
                return False, f'Falta {arma} para el {aventurero}'

    return True, 'Co-dependencia válida'

def validar_aventureros_unicos (aventureros_evento: dict):
    '''
    Docstring for validar_aventureros_unicos
    '''
    for aventurero, cantidad in aventureros_evento.items():
        if cantidad > 1:
            return False, f'No se permiten multiples {aventurero}s en el mismo evento'
    return True, 'Aventureros unicos validados'

def validar_compatibilidad_aventurero_arma(aventureros_evento: dict, armas_evento: dict):
    '''
    Docstring for validar_compatibilidad_aventurero_arma
    '''
    compatibilidad = {
        'guerrero': ['Espada Larga', 'Escudo de Hierro'],
        'mago': ['Báculo Arcano'],
        'sanador': ['Báculo Sanador'],
        'arquero': ['Arco de Roble'],
        'picaro': ['Dagas Dobles']
    }

    armas_permitidas = set()

    for aventurero, cantidad in aventureros_evento.items():
        if cantidad > 0 and aventurero in compatibilidad:
            armas_permitidas.update(compatibilidad[aventurero])

    for arma, cantidad in armas_evento.items():
        if cantidad > 0 and arma not in armas_permitidas:
            return False, f'El arma {arma} no es compatible con los aventureros seleccionados'

    return True, 'Compatibilidad aventurero-arma válida'