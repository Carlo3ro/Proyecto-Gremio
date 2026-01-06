# ===========================================
#      ALMACEN DEL GREMIO - RECURSOS
# ===========================================

# recursos.py
# Este modulo contiene la base de datos de recursos del gremio:
# aventureros, armas y mazmorras disponibles.

recursos = {
    'Aventureros': 
    {
        'Guerrero': 
            {
                'cantidad': 0,
                'cantidad_max': 3,
                'arma_predilecta': ['Espada Larga', 'Escudo de Hierro'],
                'descripcion': 'Combatientes cuerpo a cuerpo, símbolo de fuerza y liderazgo.'
            },
        'Mago': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Baculo Magico'],
                'descripcion': 'Eruditos del gremio, dominan las artes arcanas y la magia ofensiva.'
            },
        'Sanador': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Baculo Sanador'],
                'descripcion': 'Canalizan la energía divina para curar y proteger a sus aliados.'
            },
        'Arquero': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Arco de Roble'],
                'descripcion': 'Expertos del combate a distancia, veloces y precisos.'
            },
        'Picaro': 
            {
                'cantidad': 2,
                'cantidad_max': 2,
                'arma_predilecta': ['Dagas Dobles'],
                'descripcion': 'Maestros del sigilo, las trampas y la infiltración.'
            }
    },

    'Armas': 
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

    'Mazmorras': 
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

# pequenas funciones de gestion de recursos utiles

def mostrar_aventureros ():
    '''
    Muestra la cantidad de Aventureros disponibles, el arma predilecta
    y la descripcion 
    '''
    for aventurero, info in recursos['Aventureros'].items():
        if info['cantidad'] > 0:
            armas = ', '.join(info['arma_predilecta'])
            print(f'''{aventurero}: hay {info['cantidad']} disponibles, utiliza como arma: {armas},
 {info['descripcion']}\n''')
        else:
            print(f'{aventurero} no se encuentra disponible\n')
    return ''

def mostrar_armas ():
    '''
    Muestra la cantidad de Armas disponibles, el tipo de Aventurero 
    que la usa y la descripcion 
    '''
    for arma, info in recursos['Armas'].items():
        if info['cantidad'] > 0:
            print(f'''{arma}: hay {info['cantidad']} disponibles, lo utiliza: {info['tipo']},
 {info['descripcion']}\n''')
        else:
            print(f'{arma} no se encuentra disponible\n')
    return ''

def mostrar_mazmorras():
    '''
    Muestra las Mazmorras disponibles, su duracion en horas
    y su descripcion
    '''
    for mazmorra, info in recursos['Mazmorras'].items():
        if info['disponible'] == True:
            print(f'''{mazmorra}: se encuentra disponible, tarda {info['duracion_horas']} horas en completarse,
 {info['descripcion']}\n''')
        else:
            print(f'{mazmorra} no se encuentra disponible\n')
    return ''

def mostrar_recursos_disponibles():
    '''
    Muestra los héroes, armas y mazmorras disponibles.
    '''
    f1 = mostrar_aventureros()
    f2 = mostrar_armas()
    f3 = mostrar_mazmorras()
    f4 = f'\n{f1}\n{f2}\n{f3}\n'
    
    return ''

def usar_recurso(tipo, nombre, cantidad):
    '''
    Resta una cifra a la cantidad de un recurso
    verifica si es menor a la cantidad disponible
    '''
    if tipo not in recursos:
        return False
    if nombre not in recursos[tipo]:
        return False
    if recursos[tipo][nombre]['cantidad'] < cantidad:
        return False
    recursos[tipo][nombre]['cantidad'] -= cantidad

def liberar_recurso(tipo, nombre, cantidad):
    '''
    Suma una cifra a la cantidad de un recurso
    verifica si es mayor a la cantidad total
    '''
    if tipo not in recursos:
        return False
    if nombre not in recursos[tipo]:
        return False
    if recursos[tipo][nombre]['cantidad'] + cantidad > recursos[tipo][nombre]['cantidad_total']:
        return False
    recursos[tipo][nombre]['cantidad'] += cantidad

def ocupar_mazmorra(mazmorra_name):
    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra_name not in recursos['Mazmorras']:
        return False
    if not recursos['Mazmorras'][mazmorra_name]['disponible']:
        return False
    
    recursos['Mazmorras'][mazmorra_name]['disponible'] = False

    return True

def liberar_mazmorra(mazmorra_name):
    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra_name not in recursos['Mazmorras']:
        return False
    if recursos['Mazmorras'][mazmorra_name]['disponible']:
        return False
    
    recursos['Mazmorras'][mazmorra_name]['disponible'] = True

    return True