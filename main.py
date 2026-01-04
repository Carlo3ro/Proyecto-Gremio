# ===========================================
# GREMIO DE AVENTUREROS - MENÚ PRINCIPAL
# ===========================================

# Importaciones de los módulos del proyecto
import recursos

# ===========================================
# FUNCIÓN PRINCIPAL
# ===========================================

def mostrar_menu():
    '''
    Muestra el menú principal del gremio y gestiona la selección del usuario.
    '''
    while True:
        print('\n' + '='*45)
        print('GREMIO DE AVENTUREROS - MENÚ PRINCIPAL')
        print('='*45)
        print('1. Ver recursos disponibles')
        print('2. Planificar una nueva expedición')
        print('3. Consultar eventos activos')
        print('4. Pasar al día siguiente / Avanzar tiempo')
        print('5. Guardar progreso (Ir a la posada a dormir)')
        print('6. Salir del gremio')
        print('='*45)
        
        opcion = input('Selecciona una opción (1-6): ')

        if opcion == '1':
            recursos.mostrar_recursos_disponibles()
        elif opcion == '2':
            planificar_expedicion()
        elif opcion == '3':
            consultar_eventos_activos()
        elif opcion == '4':
            avanzar_tiempo_gremio()
        elif opcion == '5':
            guardar_progreso()
        elif opcion == '6':
            salir_del_gremio()
            break
        else:
            print('\nOpción no válida. Intenta de nuevo.')

# ===========================================
# FUNCIONES DEL MENÚ
# ===========================================

def planificar_expedicion():
    '''
    Permite crear una nueva expedición (evento).
    Debe pedir al usuario la mazmorra, los héroes y las armas.
    '''
    print('\n=== PLANIFICAR EXPEDICIÓN ===')
    print('Aquí se pedirá la mazmorra, héroes y armas.')
    # TODO:
    # 1. Pedir datos al usuario
    # 2. Validar con validacion.py
    # 3. Registrar evento con eventos.py


def consultar_eventos_activos():
    '''
    Muestra la lista de expediciones en curso.
    '''
    print('\n=== EVENTOS ACTIVOS ===')
    print('Aquí se listarán las expediciones activas.')
    # TODO: Leer eventos desde eventos.py o persistencia.json
    # listar_eventos()


def avanzar_tiempo_gremio():
    '''
    Avanza el tiempo del sistema.
    Permite al usuario decidir cuántas horas o días pasar.
    '''
    print('\n=== AVANZAR TIEMPO ===')
    print('Aquí se podrá avanzar el tiempo dentro del gremio.')
    # TODO:
    # 1. Pedir cantidad de horas o días
    # 2. Actualizar eventos y liberar recursos terminados
    # avanzar_tiempo()


def guardar_progreso():
    '''
    Guarda el estado actual del gremio (recursos, eventos, tiempo).
    '''
    print('\nGuardando progreso...')
    print('Has ido a la posada a descansar. El progreso se ha guardado.')
    # TODO:
    # 1. Guardar datos actuales en persistencia.json
    # guardar_datos()


def salir_del_gremio():
    '''
    Sale del programa.
    '''
    print('\nEl gremio cierra sus puertas por hoy...')
    print('¡Hasta la próxima expedición, aventurero!\n')
    # guardar = input('¿Deseas guardar antes de salir? (s/n): ')
    # if guardar.lower() == 's':
    #     guardar_progreso()

# ===========================================
# PUNTO DE ENTRADA
# ===========================================
if __name__ == '__main__':
    mostrar_menu()
