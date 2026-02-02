# ===========================================
#        LIBRO DE REGISTRO - EVENTOS
# ===========================================

# eventos.py
# Este modulo gestiona la creacion y el ciclo de vida de 
# los eventos (expediciones)

# IMPORTACIONES
import recursos
import validacion
import recompensas

# ===========================================
#           FUNCIONES DE EVENTOS
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

    # OBTENER LA DIFICULTAD
    dificultad = recursos.obtener_dificultad_mazmorra(mazmorra)

    # CREAR EVENTO
    id_evento = siguiente_id
    evento = {
        'id': id_evento,
        'mazmorra': mazmorra,
        'dificultad': dificultad,
        'recursos_usados': recursos_usados,
        'inicio': inicio_hora,
        'fin': fin_hora,
        'tiempo_restante': duracion_horas,
        'estado': 'activo'
    }

    # REGISTRAR EVENTO
    eventos_activos[id_evento] = evento

    return True, id_evento

def finalizar_evento(id_evento: int, eventos_activos: dict, eventos_historial: dict, stock: dict):
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
    
    # RECOMPENSAS
    recompensas_evento = recompensas.generar_recompensas(evento['dificultad'])
    recursos.aplicar_recompensas(recompensas_evento, stock)

    print('\nRecompensas obtenidas:')
    for nombre, cant in recompensas_evento.items():
        print(f'- {nombre} x{cant}')

    input('\nPulsa enter para continuar...')

    # FINALIZACION DE EVENTO
    evento['estado'] = 'finalizado'
    eventos_historial[id_evento] = evento

    return True, f'Evento {id_evento} finalizado correctamente'

# ===========================================
#            GESTION DE TIEMPO
# ===========================================

def avanzar_tiempo(horas: int, estado: dict):

    eventos_activos = estado['eventos_activos']
    eventos_historial = estado['eventos_historial']
    stock = estado['stock']
    reloj = estado['reloj']

    if horas <= 0:
        return []

    eventos_finalizados = []

    for _ in range(horas):
        continuar = avanzar_una_hora(reloj)

        if not continuar:
            break

        tiempo_actual = reloj['dia'] * 24 + reloj['hora']

        for id_evento, evento in list(eventos_activos.items()):
            if evento['fin'] <= tiempo_actual:
                finalizar_evento(
                    id_evento,
                    eventos_activos,
                    eventos_historial,
                    stock
                )
                eventos_finalizados.append(id_evento)

    return eventos_finalizados
    
def es_noche(hora: int) -> bool:
    # Noche de 18 a 6
    return hora >= 18 or hora < 6

def es_noche_profunda(hora: int) -> bool:
    # Noche profunda de 20 a 4
    return hora >= 20 or hora < 4

def avanzar_una_hora(reloj: dict) -> bool:
    '''
    Avanza el reloj una hora
    Devuelve False si el jugador decide obtener la espera
    ''' 
    hora_anterior = reloj['hora']
    era_noche = es_noche(hora_anterior)
    era_noche_profunda = es_noche_profunda(hora_anterior)

    reloj['hora'] += 1

    if reloj['hora'] >= 24:
        reloj['hora'] = 0
        reloj['dia'] += 1

    # CAE LA NOCHE
    if not era_noche and es_noche(reloj['hora']):
        print('\nLa noche cae sobre el gremio')
        print('Las sombras se alargan y el ambiente se vuelve mas denso')
        input('Pulsa ENTER para continuar...')

    # NOCHE PROFUNDA
    if not era_noche_profunda and es_noche_profunda(reloj['hora']):
        print('\nSientes nuevas presencias emerger de la oscuridad...')
        print('Una mazmorra especial ha aparecido')
        opcion = input('Deseas dejar de esperar para investigarlo? (s/n)').strip().lower()
        if opcion == 's':
            return False

    # AMANECE  
    if reloj['hora'] == 6:
        print('\nEl sol vuelve a alzarse, un nuevo dia comienza')
        input('Presiona ENTER para continuar')
    
    return True
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