# ===========================================
#        LIBRO DE REGISTRO - EVENTOS
# ===========================================

# eventos.py
# Este modulo gestiona la creacion y el ciclo de vida de 
# los eventos (expediciones)

# IMPORTACIONES
import recursos
import validacion

# ===========================================
#           FUNCIONES DE GESTION 
# ===========================================

def crear_evento(
    mazmorra: str,
    recursos_usados: dict,
    duracion_horas: int,
    reloj: dict,
    siguiente_id: int,
    eventos_activos: dict
):
    """
    Intenta crear un evento (expedición).
    Retorna:
        (True, id_evento) si se creó
        (False, mensaje_error) si falló
    """

    # VALIDACION 
    ok, msg = validacion.validar_evento(
        mazmorra,
        recursos_usados,
        duracion_horas,
    )
    if not ok:
        return False, msg 
    
    # OCUPAR RECURSOS
    recursos.ocupar_mazmorra(mazmorra)

    for tipo, recursos_tipo in recursos_usados.items():
        for nombre, cantidad in recursos_tipo.items():
            recursos.usar_recurso(tipo, nombre, cantidad)
    
    # CALCULAR DIN DEL EVENTO
    inicio_hora = reloj['dia'] * 24 + reloj['hora']
    fin_hora = inicio_hora + duracion_horas

    # CREAR EVENTO
    id_evento = siguiente_id
    evento = {
        'id': id_evento,
        'mazmorra': mazmorra,
        'recursos_usados': recursos_usados,
        'inicio': inicio_hora,
        'fin': fin_hora,
        'tiempo_restante': duracion_horas,
        'estado': 'activo'
    }

    # REGISTRAR EVENTO
    eventos_activos[id_evento] = evento

    return True, id_evento

def finalizar_evento(id_evento: int, eventos_activos: dict, eventos_historial: dict):
    '''
    Finaliza eventos q pasan a ser guardados en el historial de evntos
    '''
    evento = eventos_activos.pop(id_evento)

    # LIBERAR MAZMORRA

    recursos.liberar_mazmorra(evento['mazmorra'])

    # LIBERAR RECURSOS USADOS

    for tipo, aventurero_o_arma in evento['recursos_usados'].items():
        for nombre, cantidad in aventurero_o_arma.items():
            recursos.liberar_recurso(tipo, nombre, cantidad)
    
    # FINALIZACION DE EVENTO

    evento['estado'] = 'finalizado'
    eventos_historial[id_evento] = evento

    return True, f'Evento {id_evento} finalizado correctamente'

def avanzar_tiempo(horas: int, reloj: dict, eventos_activos: dict, eventos_historial: dict):
    '''
    Restar tiempo a los eventos activos, detecta eventos terminados
    y los finaliza automaticamente
    '''
    if horas <= 0:
        return []
    
    # AVANZAR TIEMPO
    reloj['hora'] += horas

    while reloj['hora'] >= 24:
        reloj['hora'] -= 24
        reloj['dia'] += 1

    tiempo_actual = reloj['dia'] * 24 + reloj['hora']

    eventos_finalizados = []

    # DETECTAR EVENTOS TERMINADOS

    for id_evento, evento in list(eventos_activos.items()):
        if evento['fin'] <= tiempo_actual:
            finalizar_evento(
                id_evento,
                eventos_activos,
                eventos_historial
            )
            eventos_finalizados.append(id_evento)
    

    return eventos_finalizados
    
# ===========================================
#           FUNCIONES DE LISTADO
# ===========================================

def listar_eventos_activos(eventos_activos: dict):
    '''
    Mostrar eventos activos
    '''
    if not eventos_activos:
        print('No hay eventos activos')
        return

    print('\n=== EVENTOS ACTIVOS ===')
    for id_evento, evento in eventos_activos.items():
        print(f'''
ID: {id_evento}
Mazmorra: {evento['mazmorra']}
Tiempo restante: {evento['tiempo_restante']}horas
Estado: {evento['estado']}
''')

def listar_historial(eventos_historial: dict):
    '''
    Mostrar expediciones finalizadas
    '''
    return list(eventos_historial.values())