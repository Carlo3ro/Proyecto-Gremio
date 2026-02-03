# ===========================================
#   GREMIO DE AVENTUREROS - MENÚ PRINCIPAL
# ===========================================

# IMPORTACIONES
import recursos
import eventos
import persistencia

# ===========================================
#         INICIALIZACION DEL ESTADO
# ===========================================

def crear_estado_inical():
    return {
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
if estado is None:
    estado = crear_estado_inical()

# ===========================================
#            FUNCIÓN PRINCIPAL
# ===========================================

def mostrar_menu(estado: dict):
    '''
    Muestra el menú principal del gremio y gestiona la selección del usuario.
    '''
    ejecutando = True

    while ejecutando:
        print('\n' + '='*45)
        print('GREMIO DE AVENTUREROS - MENÚ PRINCIPAL')
        print('='*45)
        print('1. Gestionar expediciones')
        print('2. Ver recursos disponibles')
        print('3. Ver estadisticas')
        print('4. Avanzar tiempo')
        print('5. Guardar progreso (Ir a la posada)')
        print('6. Salir del gremio')
        print('='*45)
        
        opcion = input('Selecciona una opción (1-6): ')

        if opcion == '1':
            menu_expediciones(estado)

        elif opcion == '2':
            menu_recursos(estado)

        elif opcion == '3':
            menu_estadisticas(estado)

        elif opcion == '4':
            avanzar_tiempo_gremio()

        elif opcion == '5':
            persistencia.guardar_estado(estado)
            print('\nHas descansado en la posada. Progreso guardado.')

        elif opcion == '6':
            ejecutando = confirmar_salida(estado)

        else:
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
        persistencia.guardar_estado(estado)
        print('\nProgreso guardado. Hasta la Proxima!')
        return False
    
    elif opcion == '2':
        print('\nSales del gremio sin guardar')
        return False
    
    elif opcion == '0':
        return True
    
    else:
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

    print('\n'*4) 
    eventos.mostrar_panel_expedicion(mazmorra,{},{})
        
    # DURACIÓN
    duracion_horas = recursos.obtener_duracion_mazmorra(mazmorra)
    
    # AVENTUREROS
    aventureros = recursos.seleccionar_aventureros()
    if not aventureros:
        print('No se seleccionaron aventureros')

    print('\n'*4)
    eventos.mostrar_panel_expedicion(mazmorra,aventureros,{})

    # ARMAS
    print('\nCada aventurero debe tener un arma compatible')
    armas = recursos.seleccionar_armas()
    if not armas:
        print('No se seleccionaron armas')
        return
    
    print('\n'*4)
    eventos.mostrar_panel_expedicion(mazmorra,aventureros,armas)

    input('\nPresiona ENTER para terminar la expedicion')

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
        print(f'\nError: {resultado}')
        return

    print(f'\nExpedición creada con ID {resultado}')

    # ACTUALIZAR ESTADO GLOBAL
    estado['siguiente_id'] += 1

def consultar_eventos_activos():
    evento = eventos.listar_eventos_activos(estado['eventos_activos'])
    if not evento:
        print('\nNo hay expediciones activas')
        return
    
    print('\n=== EVENTOS ACTIVOS ===')
    for i in evento:
        print(
            f'ID {i['id']} | Mazmorra: {i['mazmorra']} |'
            f'Tiempo restante: {i['tiempo restante']}h'
        )

def avanzar_tiempo_gremio():
    print('=== AVANZAR TIEMPO ===')

    while True:

        entrada = input('\nCuantas horas deseas avanzar?: ').strip()
        
        if not entrada.isdigit():
            print('\nOpcion Invalida')
            continue

        horas = int(entrada)

        if horas <= 0:
            print('\nOpcion Incorrecta')
            continue
        
        break

    finalizados = eventos.avanzar_tiempo(horas, estado)

    if finalizados:
        print(f'Se finalizaron {len(finalizados)} expediciones')
    else:
        print('No termino ninguna expedicion')

def mostrar_stock(stock: dict):
    print('\n=== STOCK ===')
    if not stock:
        print('\nEl stock esta vacio')
        input('\nPresiona ENTER para continuar...')
        return
    
    for nombre, cantidad in stock.items():
        print(f'- {nombre}: x{cantidad}')

def mostrar_historial_items_raros(estado):
    historial =  estado['estadisticas']['items_raros_obtenidos']

    print('\n=== HISTORIAL DE ITEMS RAROS ===\n')

    if not historial:
        print('Aun no has obtenido items raros')
        input('\nPresiona ENTER para volver...')
        return
    
    for idx, h in enumerate(historial, start=1):
        print(
            f'{idx}. Dia {h['dia']} - {h['hora']}:00 |'
            f' Mazmorra: {h['mazmorra']}'
            f' (Dificultad {h['dificultad']})'
        )
    input('\nPresiona ENTER para continuar')

def mostrar_resumen_estadisticas(estado: dict):
    est = estado['estadisticas']

    print('\n--- RESUMEN DEL GREMIO ---')
    print(f'Expediciones totales     : {est['expediciones_totales']}')
    print(f'Expediciones exitosas    : {est['expediciones_exitosas']}')
    print(f'Expediciones fallidas    : {est['expediciones_fallidas']}')
    print(f'Horas transcurridas      : {est['horas_transcurridas']}')
    print(f'Recompensas obtenidas    : {est['recompensas_totales']}')
    print(f'Ítems raros obtenidos    : {est['items_raros_total']}')
    print(f'Expediciones nocturnas   : {est['expediciones_noche_profunda']}')
    print(f'Mazmorras S completadas  : {est['mazmorras_S_completadas']}')

    input('\nPulsa ENTER para volver...')

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
            mostrar_resumen_estadisticas(estado)
        elif opcion == '2':
            mostrar_historial_items_raros(estado)
        elif opcion == '0':
            break
        else:
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
            recursos.mostrar_aventureros()
        elif opcion == '2':
            recursos.mostrar_armas()
        elif opcion == '3':
            recursos.mostrar_mazmorras(estado['reloj'])
        elif opcion == '4':
            mostrar_stock(estado['stock'])
        elif opcion == '0':
            break
        else:
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
            planificar_expedicion()
        elif opcion == '2':
            eventos.listar_eventos_activos(estado['eventos_activos'])
        elif opcion == '3':
            eventos.listar_historial_expediciones(estado)
        elif opcion == '0':
            break
        else:
            print('\nOpción inválida')

# ===========================================
#            PUNTO DE ENTRADA
# ===========================================

if __name__ == '__main__':
    mostrar_menu(estado)
