# ===========================================
#      ALMACEN DEL GREMIO - RECURSOS
# ===========================================

# recursos.py
# Este modulo contiene la base de datos de recursos del gremio:
# aventureros, armas y mazmorras disponibles.

# ===========================================
#           TABLA DE RECURSOS
# ===========================================

recursos = {
    'aventureros': 
    {
        'guerrero': 
            {
                'cantidad': 3,
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
            'cantidad': 4,
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
        },
        'Abismo Nocturno':
        {
            'disponible': True,
            'dificultad': 'S',
            'duracion_horas': 8,
            'nocturna': True,
            'bonus_rareza': 2.0,
            'recompensas': {
                'oro': (30, 60),
                'gema_rara': (0, 1),
                'reliquia antigua': (0, 1)
            },
            'descripcion': 'Una grieta sin fondo que solo se abre bajo la luz de la luna'
        }
    }
}

# ===========================================
#        FUNCIONES DE MOSTAR RECURSOS
# ===========================================

def mostrar_aventureros():
    print('\n=== AVENTUREROS DISPONIBLES ===\n')

    if not recursos['aventureros']:
        print('No hay aventureros registrados')
        return
    
    for nombre, datos in recursos['aventureros'].items():
        if datos['cantidad'] <= 0:
            print(f'-{nombre}: No disponible\n')
        else:
            print(f'''- {nombre} | Cantidad: {datos['cantidad']}
{datos['descripcion']}\n''')

def mostrar_armas():
    print('\n=== ARMAS DISPONIBLES ===\n')

    if not recursos['armas']:
        print('No hay armas registradas')
        return
    
    for nombre, datos in recursos['armas'].items():
        if datos['cantidad'] <= 0:
            print(f'''-{nombre}: No disponible\n''')
        else:
            print(f'''- {nombre} | Cantidad: {datos['cantidad']}
{datos['descripcion']}\n''')

def mostrar_mazmorras(reloj: dict):

    mazmorras = obtener_mazmorras_disponibles(reloj)
    
    if not mazmorras:
        print('No hay mazmorras disponibles en este momento')
        return
    
    print('\n=== MAZMORRAS DISPONIBLES ===')
    for nombre, info in mazmorras.items():
        if info['disponible'] == False:
            print(f'-{nombre} no esta disponible')
        else:
            print(f'''-{nombre} | Dificultad: {info['dificultad']}
{info['descripcion']}\n''')

def mostrar_recursos_disponibles(reloj: dict):
    mostrar_aventureros()
    mostrar_armas()
    mostrar_mazmorras(reloj)

# ===========================================
#          FUNCIONES DE GESTION 
# ===========================================

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
    if recursos[tipo][nombre]['cantidad'] + cantidad > recursos[tipo][nombre]['cantidad_max']:
        return False, 'No se pueden liberar mas recursos de los existentes'
    recursos[tipo][nombre]['cantidad'] += cantidad
    return True, 'Recurso liberado correctamente'

def ocupar_mazmorra(mazmorra: str):
    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra not in recursos['mazmorras']:
        return False, 'Mazmorra no existe'
    if not recursos['mazmorras'][mazmorra]['disponible']:
        return False, 'La mazmorra ya esta ocupada'
    
    recursos['mazmorras'][mazmorra]['disponible'] = False

    return True, 'Mazmorra ocupada correctamente'

def liberar_mazmorra(mazmorra: str):

    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra not in recursos['mazmorras']:
        return False, 'Mazmorra no existe'
    if recursos['mazmorras'][mazmorra]['disponible']:
        return False, 'Mamorra ya esta libre'
    
    recursos['mazmorras'][mazmorra]['disponible'] = True

    return True, 'Mazmorra liberada correctamente'

def aplicar_recompensas(recompensas_evento: dict, stock: dict):
    for nombre, cantidad in recompensas_evento.items():
        stock[nombre] = stock.get(nombre, 0) + cantidad
        
# ===========================================
#         NUMERADORES DE RECURSOS
# ===========================================

def seleccionar_mazmorra(reloj: dict):
    mazmorras_disponibles = obtener_mazmorras_disponibles(reloj)

    if not mazmorras_disponibles:
        return None, 'No hay mazmorras disponibles en este momento'

    nombres = list(mazmorras_disponibles.keys())

    print('\n=== MAZMORRAS DISPONIBLES ===')
    for i, nombre in enumerate(nombres, start=1):
        dificultad = mazmorras_disponibles[nombre]['dificultad']
        print(f'{i}. {nombre} (Dificultad {dificultad})')

    opcion = input('Selecciona una mazmorra: ').strip()

    if not opcion.isdigit():
        return None, 'Entrada inválida'

    idx = int(opcion) - 1

    if idx < 0 or idx >= len(nombres):
        return None, 'Opción fuera de rango'

    return nombres[idx], None

def seleccionar_aventureros() -> dict:

    aventureros_disponibles = obtener_aventureros_disponibles()

    if not aventureros_disponibles:
        print('No hay aventureros disponibles')
        return None
    
    seleccionados = {}

    nombres = list(aventureros_disponibles.keys())

    while True:
        print('\n=== AVENTUREROS DISPONIBLES ===')
        for idx, nombre in enumerate(nombres, start=1):
            if nombre not in seleccionados:
                print(f'{idx}. {nombre}')

        opcion = input('Elija el numero del Aventurero (enter para terminar la seleccion): ').strip()
        if opcion == '':
            break

        if not opcion.isdigit():
            print('Debes ingresar un número')
            continue

        idx = int(opcion) - 1
        
        if idx < 0 or idx >= len(aventureros_disponibles):
            print('Opción fuera de rango')
            continue

        nombre = nombres[idx]

        if nombre in seleccionados:
            print('Ese aventurero ya fue seleccionado')
            continue

        seleccionados[nombre] = 1

    return seleccionados

def seleccionar_armas() -> dict:

    armas_disponibles = obtener_armas_disponibles()

    if not armas_disponibles:
        print('No hay armas disponibles')
        return None

    seleccionados = {}

    nombres = list(armas_disponibles.keys())

    while True:
        print('\n=== ARMAS DISPONIBLES ===')
        for idx, nombre in enumerate(armas_disponibles, start=1):
            if nombre not in seleccionados:    
                print(f'{idx}. {nombre}')

        opcion = input('Elija el numero del Arma (enter para terminar la seleccion): ').strip()
        if opcion == '':
            break

        if not opcion.isdigit():
            print('Debes ingresar un número')
            continue

        idx = int(opcion) - 1
        if idx < 0 or idx >= len(armas_disponibles):
            print('Opción fuera de rango')
            continue

        nombre = nombres[idx]

        if nombre in seleccionados:
            print('Esa arma ya fue seleccionada')
            continue
            
        seleccionados[nombre] = 1

    return seleccionados

# ===========================================
#      FUNCIONES DE OBTENER RECURSOS 
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

def obtener_mazmorras_disponibles(reloj: dict) -> dict:
    disponibles = {}

    hora = reloj['hora']

    for nombre, info in recursos['mazmorras'].items():
        if info.get('nocturna'):
            hora = reloj['hora']
            if not hora >= 20 or hora <= 4:
                continue
        disponibles[nombre] = info

    return disponibles

def obtener_duracion_mazmorra(mazmorra: str) -> int:
    return recursos['mazmorras'][mazmorra]['duracion_horas']

def obtener_dificultad_mazmorra(mazmorra) -> str:
    return recursos['mazmorras'][mazmorra]['dificultad']

def obtener_todas_las_mazmorras():
    return recursos['mazmorras']

def obtener_recursos_disponibles():
    return {
        'aventureros': obtener_aventureros_disponibles(),
        'armas': obtener_armas_disponibles(),
        'mazmorras': obtener_mazmorras_disponibles()
    }
