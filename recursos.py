# ===========================================
#      ALMACEN DEL GREMIO - RECURSOS
# ===========================================

# recursos.py
# Este módulo contiene la base de datos de recursos del gremio:
# aventureros, armas y mazmorras disponibles.

recursos = {
    'Aventureros': 
    {
        'Guerrero': 
            {
                'cantidad': 0,
                'arma_predilecta': ['Espada Larga', 'Escudo de Hierro'],
                'descripcion': 'Combatientes cuerpo a cuerpo, símbolo de fuerza y liderazgo.'
            },
        'Mago': 
            {
                'cantidad': 2,
                'arma_predilecta': ['Baculo Magico'],
                'descripcion': 'Eruditos del gremio, dominan las artes arcanas y la magia ofensiva.'
            },
        'Sanador': 
            {
                'cantidad': 2,
                'arma_predilecta': ['Baculo Sanador'],
                'descripcion': 'Canalizan la energía divina para curar y proteger a sus aliados.'
            },
        'Arquero': 
            {
                'cantidad': 2,
                'arma_predilecta': ['Arco de Roble'],
                'descripcion': 'Expertos del combate a distancia, veloces y precisos.'
            },
        'Picaro': 
            {
                'cantidad': 2,
                'arma_predilecta': ['Dagas Dobles'],
                'descripcion': 'Maestros del sigilo, las trampas y la infiltración.'
            }
    },

    'Armas': 
    {
        'Espada Larga': 
        {
            'cantidad': 0,
            'descripcion': 'Armas versátiles para los guerreros.',
            'tipo': 'Guerrero'
        },
        'Escudo de Hierro': 
        {
            'cantidad': 2,
            'descripcion': 'Protege a los combatientes en primera línea.',
            'tipo': 'Guerrero'
        },
        'Baculo Magico': 
        {
            'cantidad': 2,
            'descripcion': 'Conduce la energía mágica de los magos.',
            'tipo': 'Mago'
        },
        'Baculo Sanador': 
        {
            'cantidad': 2,
            'descripcion': 'Canal de poder divino para los sanadores.',
            'tipo': 'Sanador'
        },
        'Arco de Roble': 
        {
            'cantidad': 2,
            'descripcion': 'Armas de precisión para los arqueros.',
            'tipo': 'Arquero'
        },
        'Dagas Dobles': 
        {
            'cantidad': 3,
            'descripcion': 'Armas ligeras para ataques rápidos y sigilosos.',
            'tipo': 'Picaro'
        }
    },

    'Mazmorras': 
    {
        'Cueva del Eco': 
        {
            'disponible': False,
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


# print('\n', recursos['Aventureros']['Guerrero']['descripcion'], '\n')

# ===========================================
#          FUNCIONES DE GESTION 
# ===========================================

# pequenas funciones de gestion de recursos utiles

def mostrar_aventureros ():
    '''
    Muestra la cantidad de Aventureros disponibles, el arma predilecta
    y la descripcion 
    '''
    print('=== AVENTUREROS DISPONIBLES ===\n')
    for aventurero, info in recursos['Aventureros'].items():
        if info['cantidad'] > 0:
            armas = ', '.join(info['arma_predilecta'])
            print(f'''{aventurero}: hay {info['cantidad']} disponibles, utiliza como arma: {armas},
 {info['descripcion']}\n''')
        else:
            print(f'{aventurero} no se encuentra disponible\n')
    return ''

#print(mostrar_aventureros())

def mostrar_armas ():
    '''
    Muestra la cantidad de Armas disponibles, el tipo de Aventurero 
    que la usa y la descripcion 
    '''
    print('\n=== ARMAS DISPONIBLES ===\n')
    for arma, info in recursos['Armas'].items():
        if info['cantidad'] > 0:
            print(f'''{arma}: hay {info['cantidad']} disponibles, lo utiliza: {info['tipo']},
 {info['descripcion']}\n''')
        else:
            print(f'{arma} no se encuentra disponible\n')
    return ''

#print(mostrar_armas())

def mostrar_mazmorras():
    '''
    Muestra las Mazmorras disponibles, su duracion en horas
    y su descripcion
    '''
    print('\n=== MAZMORRAS DISPONIBLES ===\n')
    for mazmorra, info in recursos['Mazmorras'].items():
        if info['disponible'] == True:
            print(f'''{mazmorra}: se encuentra disponible, tarda {info['duracion_horas']} horas en completarse,
 {info['descripcion']}\n''')
        else:
            print(f'{mazmorra} no se encuentra disponible\n')
    return ''

#print(mostrar_mazmorras())

def mostrar_recursos_disponibles():
    '''
    Muestra los héroes, armas y mazmorras disponibles.
    '''
    print('\n=== RECURSOS DISPONIBLES ===\n')
    print('Héroes, armas y mazmorras aparecerán aquí.\n')
    f1 = mostrar_aventureros()
    f2 = mostrar_armas()
    f3 = mostrar_mazmorras()
    f4 = f'\n{f1}\n{f2}\n{f3}\n'
    
    return ''

#print(mostrar_recursos())

#def usar_recurso():

#def liberar_recurso():

#ocupar_mazmorra():

#liberar_mazmorra():