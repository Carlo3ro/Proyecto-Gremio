# ===========================================
#      ALMACEN DEL GREMIO - RECURSOS
# ===========================================

# recursos.py
# Este modulo contiene la base de datos de recursos del gremio:
# aventureros, armas y mazmorras disponibles.

recursos = {
    'aventureros': 
    {
        'guerrero': 
            {
                'cantidad': 0,
                'cantidad_max': 3,
                'arma_predilecta': ['Espada Larga', 'Escudo de Hierro'],
                'descripcion': 'Combatientes cuerpo a cuerpo, símbolo de fuerza y liderazgo.'
            },
        'mago': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Baculo Magico'],
                'descripcion': 'Eruditos del gremio, dominan las artes arcanas y la magia ofensiva.'
            },
        'sanador': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Baculo Sanador'],
                'descripcion': 'Canalizan la energía divina para curar y proteger a sus aliados.'
            },
        'arquero': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Arco de Roble'],
                'descripcion': 'Expertos del combate a distancia, veloces y precisos.'
            },
        'picaro': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Dagas Dobles'],
                'descripcion': 'Maestros del sigilo, las trampas y la infiltración.'
            }
    },

    'armas': 
    {
        'Espada Larga': 
        {
            'cantidad': 0,
            'cantidad_max': 4,
            'descripcion': 'Armas versátiles para los guerreros.',
            'tipo': 'Guerrero'
        },
        'Escudo de Hierro': 
        {
            'cantidad': 2,
            'cantidad_max': 2,
            'descripcion': 'Protege a los combatientes en primera línea.',
            'tipo': 'Guerrero'
        },
        'Baculo Magico': 
        {
            'cantidad': 2,
            'cantidad_max': 2,
            'descripcion': 'Conduce la energía mágica de los magos.',
            'tipo': 'Mago'
        },
        'Baculo Sanador': 
        {
            'cantidad': 2,
            'cantidad_max': 2,
            'descripcion': 'Canal de poder divino para los sanadores.',
            'tipo': 'Sanador'
        },
        'Arco de Roble': 
        {
            'cantidad': 2,
            'cantidad_max': 2,
            'descripcion': 'Armas de precisión para los arqueros.',
            'tipo': 'Arquero'
        },
        'Dagas Dobles': 
        {
            'cantidad': 3,
            'cantidad_max': 3,
            'descripcion': 'Armas ligeras para ataques rápidos y sigilosos.',
            'tipo': 'Picaro'
        }
    },

    'mazmorras': 
    {
        'Cueva del Eco': 
        {
            'disponible': True,
            'dificultad': 'C',
            'duracion_horas': 4,
            'descripcion': 'Mazmorra sencilla, ideal para expediciones rápidas.'
        },
        'Bosque de Sombras': 
        {
            'disponible': True,
            'dificultad': 'C',
            'duracion_horas': 6,
            'descripcion': 'Zona peligrosa repleta de bestias sigilosas.'
        },
        'Cripta del Olvido': 
        {
            'disponible': True,
            'dificultad': 'B',
            'duracion_horas': 8,
            'descripcion': 'Ruinas malditas de un antiguo templo.'
        },
        'Torre de Cristal': 
        {
            'disponible': True,
            'dificultad': 'B',
            'duracion_horas': 10,
            'descripcion': 'Bastión mágico con trampas y enigmas arcanos.'
        },
        'Templo del Viento': 
        {
            'disponible': True,
            'dificultad': 'A',
            'duracion_horas': 12,
            'descripcion': 'Santuario elevado con guardianes ancestrales.'
        }
    }
}

# ===========================================
#          FUNCIONES DE GESTION 
# ===========================================

def obtener_aventureros_disponibles():
    disponibles = {}

    for nombre, info in recursos['aventureros'].items():
        if info['cantidad'] > 0:
            disponibles[nombre] = {
                'cantidad': info['cantidad'],
                'armas': info['arma_predilecta'],
                'descripcion': info['descripcion']
            }

    return disponibles

def obtener_armas_disponibles():
    disponibles = {}

    for nombre, info in recursos['armas'].items():
        if info['cantidad'] > 0:
            disponibles[nombre] = {
                'cantidad': info['cantidad'],
                'aventurero': info['tipo'],
                'descripcion': info['descripcion']
            }

    return disponibles

def obtener_mazmorras_disponibles():
    disponibles = {}

    for nombre, info in recursos['mazmorras'].items():
        if info['disponible']:
            disponibles[nombre] = {
                'disponible': info['disponible'],
                'dificultad': info['dificultad'],
                'duracion_horas': info['duracion_horas'],
                'descripcion': info['descripcion']
            }

    return disponibles

def obtener_todas_las_mazmorras():
    return recursos['mazmorras']

def obtener_recursos_disponibles():
    return {
        'aventureros': obtener_aventureros_disponibles(),
        'armas': obtener_armas_disponibles(),
        'mazmorras': obtener_mazmorras_disponibles()
    }

def usar_recurso(tipo: str, nombre: str, cantidad: int):
    '''
    Resta una cifra a la cantidad de un recurso
    verifica si es menor a la cantidad disponible
    '''
    if tipo not in recursos:
        return False, 'Tipo de recurso invalido'
    if nombre not in recursos[tipo]:
        return False, 'Recurso no existe'
    if recursos[tipo][nombre]['cantidad'] < cantidad:
        return False, 'Cantidad insuficiente'
    recursos[tipo][nombre]['cantidad'] -= cantidad
    return True, 'Recurso utilizado correctamente'

def liberar_recurso(tipo: str, nombre: str, cantidad: int):
    '''
    Suma una cifra a la cantidad de un recurso
    verifica si es mayor a la cantidad total
    '''
    if tipo not in recursos:
        return False, 'Tipo de recurso invalido'
    if nombre not in recursos[tipo]:
        return False, 'Recurso no existe'
    if recursos[tipo][nombre]['cantidad'] + cantidad > recursos[tipo][nombre]['cantidad_total']:
        return False, 'No se pueden liberar mas recursos de los existentes'
    recursos[tipo][nombre]['cantidad'] += cantidad
    return True, 'Recurso liberado correctamente'

def ocupar_mazmorra(mazmorra_name: str):
    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra_name not in recursos['mazmorras']:
        return False, 'Mazmorra no existe'
    if not recursos['mazmorras'][mazmorra_name]['disponible']:
        return False, 'La mazmorra ya esta ocupada'
    
    recursos['mazmorras'][mazmorra_name]['disponible'] = False

    return True, 'Mazmorra ocupada correctamente'

def liberar_mazmorra(mazmorra_name: str):

    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra_name not in recursos['mazmorras']:
        return False, 'Mazmorra no existe'
    if recursos['mazmorras'][mazmorra_name]['disponible']:
        return False, 'Mamorra ya esta libre'
    
    recursos['mazmorras'][mazmorra_name]['disponible'] = True

    return True, 'Mazmorra liberada correctamente'

# ===========================================
#         NUMERADORES DE RECURSOS
# ===========================================

def seleccionar_mazmorra():

    mazmorras_disponibles = obtener_mazmorras_disponibles()

    if not mazmorras_disponibles:
        return None, 'No hay mazmorras disponibles'

    print('\n=== MAZMORRAS DISPONIBLES ===')

    for i, nombre in enumerate(mazmorras_disponibles, start=1):
        info = mazmorras_disponibles[nombre]
        print(f'{i}. {nombre}| Duración: {info['duracion_horas']}h')

    opcion = input('Mazmorra (número, enter para terminar):  ').strip()

    if not opcion.isdigit():
        return None, 'Debes ingresar un numero'
    
    idx = int(opcion)

    if idx < 1 or idx > len(mazmorras_disponibles):
        return None, 'Opcion fuera de rango'
    
    return mazmorras_disponibles[opcion - 1], None

def seleccionar_aventureros():
    seleccion = set()

    aventureros_disponibles = obtener_aventureros_disponibles()

    if not aventureros_disponibles:
        return None, 'No hay aventureros disponibles'

    print('\n=== AVENTUREROS DISPONIBLES ===')
    for i, nombre in enumerate(aventureros_disponibles, start=1):
        print(f'{i}. {nombre}')

    while True:
        opcion = input('Aventurero (número, enter para terminar): ').strip()
        if opcion == '':
            break

        if not opcion.isdigit():
            print('Debes ingresar un número')
            continue

        idx = int(opcion)
        if idx < 1 or idx > len(aventureros_disponibles):
            print('Opción fuera de rango')
            continue

        nombre = aventureros_disponibles[idx - 1]

        if nombre in seleccion:
            print('Ese aventurero ya fue seleccionado')
            continue

        seleccion.add(nombre)

    if not seleccion:
        return None, 'No se seleccionaron aventureros'

    return list(seleccion), None

def seleccionar_armas():
    seleccion = set()

    armas_disponibles = obtener_armas_disponibles()

    if not armas_disponibles:
        return [], None

    print('\n=== ARMAS DISPONIBLES ===')
    for i, nombre in enumerate(armas_disponibles, start=1):
        print(f'{i}. {nombre}')

    while True:
        opcion = input('Arma (número, enter para terminar): ').strip()
        if opcion == '':
            break

        if not opcion.isdigit():
            print('Debes ingresar un número')
            continue

        idx = int(opcion)
        if idx < 1 or idx > len(armas_disponibles):
            print('Opción fuera de rango')
            continue

        nombre = armas_disponibles[idx - 1]

        if nombre in seleccion:
            print('Esa arma ya fue seleccionada')
            continue

        seleccion.add(nombre)

    return list(seleccion), None
