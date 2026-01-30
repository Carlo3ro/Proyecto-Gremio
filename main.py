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
        'siguente_id': 1,
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
            recursos.mostrar_recursos_disponibles(estado['recursos'])

        elif opcion == '2':
            pass

        elif opcion == '3':
            eventos.listar_eventos_activos(estado['eventos_activos'])

        elif opcion == '4':
            eventos.avanzar_tiempo(
                estado['eventos_activos'],
                estado['eventos_historial'],
                estado['recursos'],
                estado['reloj']
            )
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

    global siguiente_id, eventos_activos

    print('\n=== PLANIFICAR EXPEDICIÓN ===')

    # RECURSOS
    recursos_usados = {
        'aventureros': {},
        'armas': {}
    }

    print('\n--- Aventureros ---')
    while True:
        nombre = input('Nombre del aventurero (enter para terminar): ').strip()
        if nombre == '':
            break
        cantidad = int(input('Cantidad: '))
        if cantidad > 0:
            recursos_usados['aventureros'][nombre] = cantidad

    print('\n--- Armas ---')
    while True:
        nombre = input('Nombre del arma (enter para terminar): ').strip()
        if nombre == '':
            break
        cantidad = int(input('Cantidad: '))
        if cantidad > 0:
            recursos_usados['armas'][nombre] = cantidad

    # 3. DURACIÓN
    duracion = int(input('\nDuración de la expedición (horas): '))

    # 4. CREAR EVENTO
    ok, resultado = eventos.crear_evento(
        mazmorra,
        recursos_usados,
        duracion,
        siguiente_id,
        eventos_activos
    )

    # 5. RESULTADO
    if not ok:
        print(f'\nError: {resultado}')
        return

    print(f'\nExpedición creada con ID {resultado}')
    siguiente_id += 1

# ===========================================
#            PUNTO DE ENTRADA
# ===========================================

if __name__ == '__main__':
    mostrar_menu(estado)
