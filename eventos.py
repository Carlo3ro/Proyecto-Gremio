# ===========================================
#        LIBRO DE REGISTRO - EVENTOS
# ===========================================

# eventos.py
# Este modulo gestiona la creacion y el ciclo de vida de 
# los eventos (expediciones)

# IMPORTACIONES
import recursos

# ===========================================
#          FUNCIONES DE GESTION 
# ===========================================

def crear_evento(mazmorra_name, recursos_usados, duracion_horas):
    '''
    Crea eventos q pasan a ser guardados como eventos activos
    '''
    global siguiente_id, eventos_activos

    id_evento = siguiente_id

    evento = {
        'id': id_evento,
        'mazmorra': mazmorra_name,
        'recursos_usados': recursos_usados,
        'duracion_horas': duracion_horas,
        'tiempo_restante': duracion_horas,
        'estado': 'activo'
    }

    recursos.ocupar_mazmorra(mazmorra_name)

    for tipo, aventurero_o_arma in recursos_usados.items():
        for nombre, cantidad in aventurero_o_arma.items():
            recursos.usar_recurso(tipo, nombre, cantidad)

    eventos_activos[id_evento] = evento

    siguiente_id += 1

    return id_evento

def finalizar_evento(id_evento: int, eventos_activos: dict, eventos_historial: dict):
    '''
    Finaliza eventos q pasan a ser guardados en el historial de evntos
    '''
    if id_evento not in eventos_activos:
        return False, 'Evento no existe'

    evento = eventos_activos[id_evento]

    if evento.get('estado') != 'activo':
        return False, 'El evento ya fue finalizado'

    for tipo, aventurero_o_arma in evento['recursos_usados'].items():
        for nombre, cantidad in aventurero_o_arma.items():
            recursos.liberar_recurso(tipo, nombre, cantidad)
    
    recursos.liberar_mazmorra(evento['mazmorra'])

    evento['estado'] = 'finalizado'

    eventos_historial[id_evento] = evento
    del eventos_activos[id_evento]

    return True, f'Evento {id_evento} finalizado correctamente'

def listar_eventos_activos(eventos_activos):
    '''
    Mostrar eventos activos
    '''
    if not eventos_activos:
        return []
    
    eventos_vigentes = []

    for evento in eventos_activos.values():
        if evento['estado'] == 'activo':
            eventos_vigentes.append({
                'id': evento['id'],
                'mazmorra': evento['mazmorra'],
                'tiempo_restante': evento['tiempo_restante']
            })

    return eventos_vigentes

def listar_historial(eventos_historial):
    '''
    Mostrar expediciones finalizadas
    '''
    return list(eventos_historial.values())

def avanzar_tiempo(horas: int, eventos_activos: dict, historial: dict, reloj: dict):
    '''
    Restar tiempo a los eventos activos, detecta eventos terminados
    y los finaliza automaticamente
    '''
    if horas <= 0:
        return False, "Las horas deben ser positivas"

    # Avanzar reloj
    reloj['hora'] += horas

    while reloj['hora'] >= 24:
        reloj['hora'] -= 24
        reloj['dia'] += 1

    eventos_a_finalizar = []

    for id_evento, evento in eventos_activos.items():
        if evento['estado'] != 'activo':
            continue

        evento['tiempo_restante'] -= horas

        if evento['tiempo_restante'] <= 0:
            eventos_a_finalizar.append(id_evento)

    for id_evento in eventos_a_finalizar:
        finalizar_evento(id_evento, eventos_activos, historial)

    return True, f"Tiempo avanzado {horas} horas"

# ===========================================
#                 EJEMPLOS
# ===========================================

# eventos_activos = {
#     1: {
#         'id': 1,
#         'mazmorra': 'Cripta del Olvido',
#         'recursos_usados': {
#             'aventureros': {
#                 'guerrero': 1,
#                 'mago': 1
#             },
#             'armas': {
#                 'Espada': 1,
#                 'Báculo Mágico': 1
#             }
#         },
#         'duracion_horas': 6,
#         'tiempo_restante': 6,
#         'estado': 'activo'
#     },
#     2: {
#         'id': 2,
#         'mazmorra': 'Catacumbas Antiguas',
#         'recursos_usados': {
#             'aventureros': {
#                 'arquero': 2
#             },
#             'armas': {
#                 'Arco de Roble': 2
#             }
#         },
#         'duracion_horas': 3,
#         'tiempo_restante': 3,
#         'estado': 'activo'
#     }
# }

# evento = {
#         'id': 1,
#         'mazmorra': 'Cueva del Eco',
#         'recursos_usados': recursos_usados,
#         'duracion_horas': 8,
#         'tiempo_restante': 8,
#         'estado': 'activo'
#     }

# recursos_usados = {
#       'aventureros':{
#           'guerrero': 1,
#           'sanador': 1
#       },
#       'armas':{
#           'Espada Larga': 1,
#           'Baculo Sanador': 1
#       }
#     }