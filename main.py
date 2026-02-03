# ===========================================
#   GREMIO DE AVENTUREROS - MENÚ PRINCIPAL
# ===========================================

# IMPORTACIONES
import recursos
import eventos
import persistencia
import time
from eventos import limpiar_pantalla as lp
from eventos import icono_hora

# ===========================================
#         INICIALIZACION DEL ESTADO
# ===========================================

def crear_estado_inical():
    return {
        'jugador':{
            'nombre': None
        },
        'recursos': recursos.recursos,
        'eventos_activos': {},
        'eventos_historial': {},
        'siguiente_id': 1,
        'reloj': {'dia': 1, 'hora': 8},
        'stock': {},
        'estadisticas': {
            'expediciones_totales': 0,
            'expediciones_exitosas': 0,
            'expediciones_fallidas': 0,
            'horas_transcurridas': 0,
            'recompensas_totales': 0,
            'items_raros_total': 0,
            'items_raros_obtenidos': [],
            'expediciones_noche_profunda': 0,
            'mazmorras_S_completadas': 0
        }
    }

estado = persistencia.cargar_estado()

es_partida_nueva = estado is None

if es_partida_nueva:
    estado = crear_estado_inical()

# ===========================================
#               BIENVENIDA
# ===========================================

def bienvenida(estado, es_partida_nueva):

    lp()

    nombre = estado['jugador']['nombre']

    print('='*40)
    print('        GREMIO DE AVENTUREROS')
    print('='*40)

    if es_partida_nueva:

        print('Humano...')
        time.sleep(1.5)
        nombre = input('\n Cuál es tu nombre? ').strip()
        time.sleep(1.5)

        if not nombre:
            nombre = 'Aventurero'

        estado['jugador']['nombre'] = nombre

        print(f'\nBienvenido al gremio, {nombre}.')
        time.sleep(1.5)
        print('Grandes riquezas — o una tumba gloriosa — te esperan.')
        time.sleep(1.5)

    else:

        print(f'\nEl gremio sigue en pie ⚔️, {nombre}.')
        time.sleep(1.5)
        print('Nuevas expediciones aguardan tu mando.')
        time.sleep(1.5)

    input('\nPulsa ENTER para continuar...')
    time.sleep(1.5)

bienvenida(estado, es_partida_nueva)
# ===========================================
#            FUNCIÓN PRINCIPAL
# ===========================================

def mostrar_menu(estado: dict):
    '''
    Muestra el menú principal del gremio y gestiona la selección del usuario.
    '''
    lp()
    ejecutando = True

    while ejecutando:

        reloj = estado['reloj']
        nombre = estado['jugador']['nombre']
        icono1 = icono_hora(estado['reloj']['hora'])

        print(f'🛡️  {nombre} | Día {reloj["dia"]} — {reloj["hora"]:02d}:00 {icono1}\n')
        print('='*44)
        print('GREMIO DE AVENTUREROS - MENÚ PRINCIPAL')
        print('='*44)
        print('1. Gestionar expediciones')
        print('2. Ver recursos disponibles')
        print('3. Ver estadisticas')
        print('4. Avanzar tiempo')
        print('5. Guardar progreso (Ir a la posada)')
        print('6. Salir del gremio')
        print('='*44)
        
        opcion = input('Selecciona una opción (1-6): ')

        if opcion == '1':
            lp()
            menu_expediciones(estado)

        elif opcion == '2':
            lp()
            menu_recursos(estado)

        elif opcion == '3':
            lp()
            menu_estadisticas(estado)

        elif opcion == '4':
            lp()
            avanzar_tiempo_gremio()

        elif opcion == '5':
            lp()
            persistencia.guardar_estado(estado)
            print('\nHas descansado en la posada. Progreso guardado.')

        elif opcion == '6':
            lp()
            ejecutando = confirmar_salida(estado)

        else:
            lp()
            print('\nOpcion no valida. Intenta de nuevo.')

# ===========================================
#         SALIDA CON CORFIMACION
# ===========================================  

def confirmar_salida (estado: dict) -> bool:
    print('\nDeseas guardar antes de salir?')
    print('1. Guardar y salir')
    print('2. Salir sin guardar')
    print('0. Cancelar')

    opcion = input('Selecciona una opcion (1-3): ')

    if opcion == '1':
        lp()
        persistencia.guardar_estado(estado)
        print('\nProgreso guardado. Hasta la Proxima :3!')
        return False
    
    elif opcion == '2':
        lp()
        print('\nSales del gremio sin guardar')
        return False
    
    elif opcion == '0':
        lp()
        return True
    
    else:
        lp()
        print('\nOpcion no valida')
        return True

# ===========================================
#       FUNCIONES DE LOS SUBMENUS
# ===========================================

def planificar_expedicion():

    siguiente_id = estado['siguiente_id'] 
    eventos_activos = estado['eventos_activos']
    reloj = estado['reloj']    

    print('\n=== PLANIFICAR EXPEDICIÓN ===')

    # MAZMORRA
    mazmorra, error = recursos.seleccionar_mazmorra(estado['reloj'])
    if error:
        return

    lp()
    eventos.mostrar_panel_expedicion(mazmorra,{},{})
        
    # DURACIÓN
    duracion_horas = recursos.obtener_duracion_mazmorra(mazmorra)
    
    # AVENTUREROS
    aventureros = recursos.seleccionar_aventureros()
    if not aventureros:
        print('No se seleccionaron aventureros')

    lp()
    eventos.mostrar_panel_expedicion(mazmorra,aventureros,{})

    # ARMAS
    print('\nCada aventurero debe tener un arma compatible')
    armas = recursos.seleccionar_armas()
    if not armas:
        print('No se seleccionaron armas')
        return
    
    lp()
    eventos.mostrar_panel_expedicion(mazmorra,aventureros,armas)

    # RECURSOS
    recursos_usados = {
        'aventureros': aventureros,
        'armas': armas
    }

    # CREAR EVENTO
    ok, resultado = eventos.crear_evento(
        mazmorra,
        recursos_usados,
        duracion_horas,
        reloj,
        siguiente_id,
        eventos_activos
    )

    if not ok:
        lp()
        print(f'\nError: {resultado}')
        return

    print(f'⚔️  La expedición ha sido registrada'
        f'ID del contrato: {resultado}'
    )
    input('\nPresiona ENTER para continuar...')
    lp()
    # ACTUALIZAR ESTADO GLOBAL
    estado['siguiente_id'] += 1

def avanzar_tiempo_gremio():

    print('=== AVANZAR TIEMPO ===')

    while True:

        entrada = input('\nCuantas horas deseas avanzar?: ').strip()
        
        if not entrada.isdigit():
            lp()
            print('\nOpcion Invalida')
            continue

        horas = int(entrada)

        if horas <= 0:
            lp()
            print('\nOpcion Incorrecta')
            continue
        
        break

    lp()

    eventos_antes = len(estado['eventos_activos'])

    finalizados = eventos.avanzar_tiempo(horas, estado)

    print('El tiempo transcurre...')
    time.sleep(1.0)
    print(f'Han pasado {horas}h ...')
    mostrar_reloj(estado['reloj'])
    eventos.listar_eventos_activos_reloj(estado['eventos_activos'], estado['reloj'])
    input('Presiona ENTER para continuar')
    lp()

    if eventos_antes == 0:
        lp()
        print('🛡️ El gremio está en calma...\n')
        time.sleep(1.0)
        input('Presiona ENTER para continuar')
        lp()
    elif finalizados:
        lp()
        print(f'Se finalizaron {len(finalizados)} expediciones\n')
        time.sleep(1.0)
        input('Presiona ENTER para terminar')
        lp()
    
def mostrar_stock(stock: dict):
    print('\n=== STOCK ===')
    if not stock:
        print('\nEl stock esta vacio')
        input('\nPresiona ENTER para continuar...')
        lp()
        return
    
    for nombre, cantidad in stock.items():
        print(f'- {nombre}: x{cantidad}')
    
    input('\nPresiona ENTER para continuar...')
    lp()

def mostrar_historial_items_raros(estado):
    historial =  estado['estadisticas']['items_raros_obtenidos']

    print('\n=== HISTORIAL DE ITEMS RAROS ===\n')

    if not historial:
        print('Aun no has obtenido items raros')
        input('\nPresiona ENTER para volver...')
        lp()
        return
    
    for idx, h in enumerate(historial, start=1):
        print(
            f'{idx}. Dia {h['dia']} - {h['hora']}:00 |'
            f' Mazmorra: {h['mazmorra']}'
            f' (Dificultad {h['dificultad']})'
        )
    input('\nPresiona ENTER para volver...')
    lp()

def mostrar_resumen_estadisticas(estado: dict):
    est = estado['estadisticas']

    print('\n--- RESUMEN DEL GREMIO ---')
    print(f'⚔️  Expediciones totales     : {est['expediciones_totales']}')
    print(f'🏆 Expediciones exitosas    : {est['expediciones_exitosas']}')
    print(f'💀 Expediciones fallidas    : {est['expediciones_fallidas']}')
    print(f'⏳ Horas transcurridas      : {est['horas_transcurridas']}')
    print(f'🪙  Recompensas obtenidas    : {est['recompensas_totales']}')
    print(f'💎 Ítems raros obtenidos    : {est['items_raros_total']}')
    print(f'🌙 Expediciones nocturnas   : {est['expediciones_noche_profunda']}')
    print(f'⚰️  Mazmorras S completadas  : {est['mazmorras_S_completadas']}')

    input('\nPulsa ENTER para volver...')
    lp()

def mostrar_reloj(reloj: dict):
    
    dia = reloj['dia']
    hora = reloj['hora']
    icono = icono_hora(reloj['hora'])

    print(f'=== Dia {dia} - hora {hora:02d}:00 {icono} ===')

# ===========================================
#           FUNCIONES DEl MENU
# ===========================================

def menu_estadisticas(estado: dict):

    while True:
        print('\n=== ESTADISTICAS DEL GREMIO ===')
        print('1. Resumen general')
        print('2. Items raros obtenidos')
        print('0. Volver')

        opcion = input('\nElige una opcion: ').strip()

        if opcion == '1':
            lp()
            mostrar_resumen_estadisticas(estado)
        elif opcion == '2':
            lp()
            mostrar_historial_items_raros(estado)
        elif opcion == '0':
            lp()
            break
        else:
            lp()
            print('\nOpcion Invalida')
    
def menu_recursos(estado: dict):
    while True:
        print('\n=== RECURSOS DEL GREMIO ===')
        print('1. Ver aventureros')
        print('2. Ver armas')
        print('3. Ver mazmorras')
        print('4. Ver stock de ítems')
        print('0. Volver')

        opcion = input('\nElige una opción: ').strip()

        if opcion == '1':
            lp()
            recursos.mostrar_aventureros()
        elif opcion == '2':
            lp()
            recursos.mostrar_armas()
        elif opcion == '3':
            lp()
            recursos.mostrar_mazmorras(estado['reloj'])
        elif opcion == '4':
            lp()
            mostrar_stock(estado['stock'])
        elif opcion == '0':
            lp()
            break
        else:
            lp()
            print('\nOpción inválida')

def menu_expediciones(estado: dict):
    while True:
        print('\n=== GESTIÓN DE EXPEDICIONES ===')
        print('1. Planificar nueva expedición')
        print('2. Ver expediciones activas')
        print('3. Ver historial de expediciones')
        print('0. Volver')

        opcion = input('\nElige una opción: ').strip()

        if opcion == '1':
            lp()
            planificar_expedicion()
        elif opcion == '2':
            lp()
            eventos.listar_eventos_activos(estado['eventos_activos'], estado['reloj'])
            input('Presiona ENTER para continuar')
            lp()
        elif opcion == '3':
            lp()
            eventos.listar_historial_expediciones(estado)
        elif opcion == '0':
            lp()
            break
        else:
            lp()
            print('\nOpción inválida')

# ===========================================
#            PUNTO DE ENTRADA
# ===========================================

if __name__ == '__main__':
    mostrar_menu(estado)
