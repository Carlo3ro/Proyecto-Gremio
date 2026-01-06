# ===========================================
#        LIBRO DE REGISTRO - EVENTOS
# ===========================================

# evntos.py
# Este modulo gestiona la creacion y el ciclo de vida de 
# los eventos (expediciones)

# Importaciones de los módulos del proyecto
import recursos

eventos_activos = {}
eventos_historial = {}
siguiente_id = 1

# cada evento tiene:
# - id
# - mazmorra
# - recursos_usados
# - duracion_horas
# - tiempo_restante
# - estado (activo o finalizado)

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
        "id": id_evento,
        "mazmorra": mazmorra_name,
        "recursos_usados": recursos_usados,
        "duracion_horas": duracion_horas,
        "tiempo_restante": duracion_horas,
        "estado": "activo"
    }

    recursos.ocupar_mazmorra(mazmorra_name)

    for tipo, aventureros in recursos_usados.items():
        for nombre, cantidad in aventureros.items():
            recursos.usar_recurso(tipo, nombre, cantidad)

    eventos_activos[id_evento] = evento

    siguiente_id += 1

    return id_evento

def finalizar_evento(id_evento):
    '''
    Finaliza eventos q pasan a ser guardados en el historial de evntos
    '''
    global eventos_activos, eventos_historial

    evento = eventos_activos[id_evento]

    for tipo, aventureros in evento["recursos_usados"].items():
        for nombre, cantidad in aventureros.items():
            recursos.liberar_recurso(tipo, nombre, cantidad)

    recursos.liberar_mazmorra(evento["mazmorra"])

    evento["estado"] = "finalizado"

    eventos_historial[id_evento] = evento
    del eventos_activos[id_evento]

def listar_eventos_activos():
    '''
    Mostrar o delvolver eventos activos
    '''

def listar_historial():
    '''
    Mostrar expediciones finalizadas
    '''

def avanzar_tiempo(horas):
    '''
    Restar tiempo a los eventos activos, detecta eventos terminados
    y los finaliza automaticamente
    '''
    eventos_a_finalizar = []

    for id_evento, evento in eventos_activos.items():
        evento["tiempo_restante"] -= horas
        if evento["tiempo_restante"] <= 0:
            eventos_a_finalizar.append(id_evento)

    for id_evento in eventos_a_finalizar:
        finalizar_evento(id_evento)

