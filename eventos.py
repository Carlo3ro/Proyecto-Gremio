# ===========================================
#      LIBRO DE REGISTRO - EVENTO
# ===========================================

# evntos.py
# Gestiona la creacion y el ciclo de vida de los eventos (expediciones)

# Importaciones de los módulos del proyecto
import recursos

eventos_activos = {}
eventos_historial = {}
count_id = 1

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

def crear_evento(mazmorra_name, recursos_usados, duracion):
    '''
    Crea eventos q pasan a ser guardados como eventos activos
    '''
    # - Obtener id
    # - Crear estructura del evento
    # - Ocupar mazmorra
    # - Usar recursos
    # - Guardar evento activo
    # - Incrementar ID
    # - Devolver ID

def listar_eventos_activos():
    '''
    Mostrar o delvolver eventos activos
    '''

def listar_historial():
    '''
    Mostrar expediciones finalizadas
    '''

def avanzar_tiempo():
    '''
    restar tiempo a eventos activos
    detectar eventos terminados
    finalizarlos automaticamente
    '''

def finalizar_eventos():
    '''
    liberar recursos
    liberar mazmorra
    mover evento al historial
    '''

