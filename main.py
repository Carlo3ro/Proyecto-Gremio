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
        'reloj': {'dia': 1, 'hora': 8}
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
        print('1. Ver recursos disponibles')
        print('2. Planificar una nueva expedición')
        print('3. Consultar eventos activos')
        print('4. Pasar al día siguiente / Avanzar tiempo')
        print('5. Guardar progreso (Ir a la posada)')
        print('6. Salir del gremio')
        print('='*45)
        
        opcion = input('Selecciona una opción (1-6): ')

        if opcion == '1':
            #TODO
            recursos.mostrar_recursos_disponibles()

        elif opcion == '2':
            planificar_expedicion()

        elif opcion == '3':
            eventos.listar_eventos_activos(estado['eventos_activos'])

        elif opcion == '4':
            avanzar_tiempo_gremio()
        elif opcion == '5':
            persistencia.guardar_estado(estado)
            print('\nHas descansado en la posada. Progreso guardado.')

        elif opcion == '6':
            ejecutando = confirmar_salida(estado)

        else:
            print('\nOpción no válida. Intenta de nuevo.')

# ===========================================
#         SALIDA CON CORFIMACION
# ===========================================  

def confirmar_salida (estado: dict) -> bool:
    print('\nDeseas guardar antes de salir?')
    print('1. Guardar y salir')
    print('2. Salir sin guardar')
    print('3. Cancelar')

    opcion = input('Selecciona una opcion (1-3): ')

    if opcion == '1':
        persistencia.guardar_estado(estado)
        print('\nProgreso guardado. Hasta la Proxima!')
        return False
    
    elif opcion == '2':
        print('\nSales del gremio sin guardar')
        return False
    
    elif opcion == '3':
        print('\nSalida cancelada')
        return True
    
    else:
        print('\nOpcion no valida')
        return True

# ===========================================
#           FUNCIONES DEL MENU
# ===========================================

def planificar_expedicion():

    siguiente_id = estado['siguiente_id'] 
    eventos_activos = estado['eventos_activos']
    reloj = estado['reloj']    

    print('\n=== PLANIFICAR EXPEDICIÓN ===')

    # MAZMORRA
    mazmorra, error = recursos.seleccionar_mazmorra()
    if error:
        print(error)
        return
    
    # DURACIÓN
    duracion_horas = recursos.obtener_duracion_mazmorra(mazmorra)
    
    # AVENTUREROS
    aventureros = recursos.seleccionar_aventureros()
    if not aventureros:
        print('No se seleccionaron aventureros')
    # ARMAS
    print('\nCada aventurero debe tener un arma compatible')
    armas = recursos.seleccionar_armas()
    if not armas:
        print('No se seleccionaron armas')

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

    horas = int(input('\nCuantas horas deseas avanzar?: '))

    finalizados = eventos.avanzar_tiempo(
        horas,
        estado['reloj'],
        estado['eventos_activos'],
        estado['eventos_historial'],
    )
    if finalizados:
        print(f'Se finalizaron {len(finalizados)} expediciones')
    else:
        print('No termino ninguna expedicion')
# ===========================================
#            PUNTO DE ENTRADA
# ===========================================

if __name__ == '__main__':
    mostrar_menu(estado)
