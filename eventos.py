# ===========================================
#        LIBRO DE REGISTRO - EVENTOS
# ===========================================

# eventos.py
# Este modulo gestiona la creacion y el ciclo de vida de 
# los eventos (expediciones)

# IMPORTACIONES
import time
import random
import recursos
import validacion
from recompensas import obtener_items_raros
from recompensas import generar_recompensas
from estadisticas import registrar_items_raros

# ===========================================
#           TABLA DE DIFICULTAD
# ===========================================

umbral_dificultad = {
    'F': 30,
    'D': 45,
    'C': 54,
    'B': 75,
    'A': 100,
    'S': 120
}

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
    '''
    Intenta crear un evento (expedición).
    Retorna:
        (True, id_evento) si se creó
        (False, mensaje_error) si falló
    '''

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
    
    # CALCULAR FIN DEL EVENTO
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
        'tiempo_total': duracion_horas,
        'tiempo_restante': 0,
        'estado': 'activo'
    }

    # REGISTRAR EVENTO
    eventos_activos[id_evento] = evento

    return True, id_evento

def finalizar_evento(
    id_evento: int, 
    eventos_activos: dict, 
    eventos_historial: dict, 
    stock: dict, estado: dict
    ):
    '''
    Finaliza eventos q pasan a ser guardados en el historial de eventos
    '''
    evento = eventos_activos.pop(id_evento)

    if 'resultado' in evento:
        limpiar_pantalla()
        return True, 'Evento ya fue resuelto'

    # LIBERAR MAZMORRA
    recursos.liberar_mazmorra(evento['mazmorra'])

    # LIBERAR RECURSOS USADOS
    for tipo, aventurero_o_arma in evento['recursos_usados'].items():
        for nombre, cantidad in aventurero_o_arma.items():
            recursos.liberar_recurso(tipo, nombre, cantidad)

    # RISK SCORE
    poder = calcular_poder_expedicion(
        evento['recursos_usados']['aventureros'],
        evento['recursos_usados']['armas'],
        evento['dificultad']
    )

    exito = resolver_expedicion(poder, evento['dificultad'])
    evento['exito'] = exito

    # RESULTADO DE LA EXPEDICION

    estado['estadisticas']['expediciones_totales'] += 1

    if not exito:
        print('\nLa expedicion ha fracasado...')
        time.sleep(1.5)
        print('Los aventureros regresan heridos y sin botin.')
        time.sleep(1.5)

        estado['estadisticas']['expediciones_fallidas'] += 1

    else:
        estado['estadisticas']['expediciones_exitosas'] += 1

        if evento['dificultad'] == 'S':
            estado['estadisticas']['mazmorras_S_completadas'] += 1

        # RECOMPENSAS (SOLO SI HAY ÉXITO)
        if evento.get('nocturna', False):
            bonus = 2.0
            estado['estadisticas']['expediciones_noche_profunda'] += 1
        else:
            bonus = 1.0

        recompensas_evento = generar_recompensas(evento['dificultad'], bonus)
        recursos.aplicar_recompensas(recompensas_evento, stock)

        items_raros = obtener_items_raros(recompensas_evento)

        print('\nExpedicion exitosa 🏆')
        print('\nRecompensas obtenidas:')
        for nombre, cant in recompensas_evento.items():
            if nombre not in items_raros:
                print(f'- {nombre} x{cant}')
        

        estado['estadisticas']['recompensas_totales'] += sum(recompensas_evento.values())

        # ITEMS RAROS

        if items_raros:
            registrar_items_raros(
                items_raros,
                evento,
                estado['reloj'],
                estado
            )
            estado['estadisticas']['items_raros_total'] += len(items_raros)

            print('...')
            time.sleep(2)
            print('\n💎 Algo resplandece entre los restos...\n')
            time.sleep(2)
            print('Te aproximas lentamente\n')
            time.sleep(1.5)
            print('\n???')
            time.sleep(1.5)
            for item in items_raros:
                print(f'- {item} encontrado')
                time.sleep(0.8)

    # FINALIZACION DEL EVENTO

    evento['estado'] = 'finalizado'
    evento['resultado'] = 'exitosa' if exito else 'fallida'

    eventos_historial[id_evento] = evento

    input('\nPulsa ENTER para continuar...')
    limpiar_pantalla()
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
                    stock,
                    estado
                )
                eventos_finalizados.append(id_evento)

    estado['estadisticas']['horas_transcurridas'] += horas

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
        print('\nLa noche cae sobre el gremio 🌙')
        time.sleep(1.5)
        print('Las sombras se alargan y el ambiente se vuelve mas denso\n')
        time.sleep(1.5)
        input('Pulsa ENTER para continuar...')
        time.sleep(1.5)
        limpiar_pantalla()

    # NOCHE PROFUNDA
    if not era_noche_profunda and es_noche_profunda(reloj['hora']):
        print('\nSientes nuevas presencias emerger de la oscuridad...')
        time.sleep(1.5)
        print('Una mazmorra especial ha aparecido 💀\n')
        time.sleep(1.5)

        while True:
            opcion = input('Deseas dejar de esperar para investigarlo? (s/n): ').strip().lower()
            limpiar_pantalla()
            if opcion in ('s', 'n'):
                break
            limpiar_pantalla()
            print('Ingresa solo "s" o "n"')
            

        if opcion == 's':
            return False

    # AMANECE  
    if reloj['hora'] == 6:
        limpiar_pantalla()
        print('\nEl sol vuelve a alzarse, un nuevo dia comienza ☀️')
        input('\nPresiona ENTER para continuar\n')
        limpiar_pantalla()
    return True

# ===========================================
#           FUNCIONES DE LISTADO
# ===========================================

def listar_eventos_activos(eventos_activos, reloj):
    '''
    Mostrar eventos activos
    '''
    print('\n---📜 EXPEDICIONES EN CURSO ---')
    if not eventos_activos:
        print('No hay eventos activos')
        input('\nPresiona ENTER para continuar...')
        return

    for id_evento, evento in eventos_activos.items():

        restante = calcular_tiempo_restante(evento, reloj)
        barra, porcentaje = generar_barra_progreso(evento, reloj)

        print(f'''
Expedicion #{id_evento}
Mazmorra: {evento['mazmorra']}
Dificultad: {evento['dificultad']}
Aventureros: {', '.join(evento['recursos_usados']['aventureros'])}
Tiempo total: {evento['tiempo_total']} horas
{barra} {porcentaje}% - {restante} horas restantes
''')

def listar_eventos_activos_reloj(eventos_activos, reloj):
    '''
    Mostrar eventos activos
    '''
    print('\n---📜 EXPEDICIONES EN CURSO ---')
    if not eventos_activos:
        print('No hay eventos activos')
        return

    for id_evento, evento in eventos_activos.items():

        restante = calcular_tiempo_restante(evento, reloj)
        barra, porcentaje = generar_barra_progreso(evento, reloj)

        print(f'''
Expedicion #{id_evento}
Mazmorra: {evento['mazmorra']}
Dificultad: {evento['dificultad']}
Aventureros: {', '.join(evento['recursos_usados']['aventureros'])}
Tiempo total: {evento['tiempo_total']} horas
{barra} {porcentaje}% - {restante} horas restantes
''')
        
def listar_historial_expediciones(estado: dict):
    historial = estado['eventos_historial']

    print('\n--- HISTORIAL DE EXPEDICIONES ---')

    if not historial:
        print('Aun no se han realizado expediciones.')
        input('\nPulsa ENTER para volver...')
        return

    for id_evento, evento in historial.items():
        estado_evt = evento.get('estado', 'finalizado')

        print(f'\n📜 Expedición #{id_evento}')
        print(f'  Mazmorra   : {evento['mazmorra']}')
        print(f'  Dificultad : {evento['dificultad']}')
        print(f'  Estado     : {estado_evt}')

        resultado = evento.get('resultado')

        if resultado == 'fallida':
            print('\n  💀 La expedición fracaso.')
        else:
            print('\n  🏆 La expedición tuvo exito.')

    input('\nPulsa ENTER para volver...')
    limpiar_pantalla()

# ===========================================
#           CALCULOS DE EVENTOS 
# ===========================================

def calcular_poder_expedicion(aventureros, armas, dificultad):
    poder = 0

    # Poder base por aventureros
    for nombre in aventureros:
        poder += recursos.recursos['aventureros'][nombre]['poder']

    for arma in armas:
        poder += recursos.recursos['armas'][arma]['poder']

    # Penalización por dificultad S
    if dificultad == 'S':
        poder *= 0.85

    return int(poder)

def resolver_expedicion(poder, dificultad):

    umbral = umbral_dificultad[dificultad]

    # 15% de suerte siempre
    suerte  = random.random() < 0.15

    print(f'\nPoder de tu expedicion: {poder}')
    print(f'Poder de la mazmorra: {umbral}')

    return poder >= umbral or suerte

def calcular_tiempo_restante(evento, reloj):

    tiempo_actual = reloj['dia'] * 24 + reloj['hora']
    restante = evento['fin'] - tiempo_actual

    return max(0, restante)

# ===========================================
#           FUNCIONES DE UI
# ===========================================

def mostrar_panel_expedicion(mazmorra, aventureros, armas):

    print('='*34)
    print('=========== EXPEDICIÓN ===========')
    print(f'\nMazmorra: {mazmorra} ({recursos.obtener_dificultad_mazmorra(mazmorra)})')
    print()

    # Aventureros
    print('Aventureros seleccionados (armas compatibles):')

    if not aventureros:
        print('  Ninguno')
    else:
        for nombre in aventureros:

            data_aventurero = recursos.recursos['aventureros'][nombre]
            compatibles = data_aventurero['arma_predilecta']
            poder = recursos.recursos['aventureros'][nombre]['poder']
            print(f'{nombre.title()} (+{poder}):')
            print(f'    ({", ".join(compatibles)})')

    print()

    # Armas elegidas
    print('Armas seleccionadas:')

    if not armas:
        print('  Ninguna')
    else:
        for arma in armas:
            poder = recursos.recursos['armas'][arma]['poder']
            print(f'{arma.title()} (+{poder})')

    print()

    # Poder total
    if aventureros:
        poder_total = calcular_poder_expedicion(
            aventureros,
            armas,
            recursos.obtener_dificultad_mazmorra(mazmorra)
        )

        print(f'Poder total: {poder_total}')

        # Riesgo
        umbral = umbral_dificultad[
            recursos.obtener_dificultad_mazmorra(mazmorra)
        ]

        if poder_total >= umbral:
            print('Riesgo: BAJO ✅')
        elif poder_total >= umbral * 0.8:
            print('Riesgo: MEDIO ⚠️')
        else:
            print('Riesgo: ALTO 💀')

    print('='*35)

def generar_barra_progreso(evento, reloj):

    inicio = evento['inicio']
    fin = evento['fin']

    tiempo_actual = reloj['dia'] * 24 + reloj['hora']

    duracion_total = fin - inicio
    transcurrido = tiempo_actual - inicio

    # Clamp profesional (evita negativos o >100%)
    progreso = max(0, min(1, transcurrido / duracion_total))

    bloques_totales = 10
    bloques_llenos = int(progreso * bloques_totales)

    barra = '■' * bloques_llenos + '□' * (bloques_totales - bloques_llenos)

    porcentaje = int(progreso * 100)

    return barra, porcentaje

def limpiar_pantalla():
    print('\n'*40)

def icono_hora(hora:int) -> str:
    if es_noche_profunda(hora):
        return '🌑'
    elif es_noche(hora):
        return '🌙' 
    else:
        return '☀️'