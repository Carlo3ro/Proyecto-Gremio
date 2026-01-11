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

# si la cantidad del aventurero <= 0 la def devuelve un
# dict vacio pq del for salta para el return disponibles 

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
    if mazmorra_name not in recursos['mazmorras']:
        return False
    if not recursos['mazmorras'][mazmorra_name]['disponible']:
        return False
    
    recursos['mazmorras'][mazmorra_name]['disponible'] = False

    return True

def liberar_mazmorra(mazmorra_name):
    '''
    Ocupa una mazmorra (pasa su disponibilidad a False)
    '''
    if mazmorra_name not in recursos['mazmorras']:
        return False
    if recursos['mazmorras'][mazmorra_name]['disponible']:
        return False
    
    recursos['mazmorras'][mazmorra_name]['disponible'] = True

    return True