# ===========================================
#    VERIFICACION DEL GREMIO - VALIDACION
# ===========================================

# validacion.py
# Verifica si los eventos pueden exitir en el sistema
# Guardian del sitema 

# IMPORTACIONES
import restricciones

# ===========================================
#          FUNCIONES DE VALIDACION
# ===========================================

import recursos
import restricciones

def validar_evento(
    mazmorra: str,
    recursos_usados: dict,
    duracion_horas: int,
):
    aventureros_evento = recursos_usados.get('aventureros', {})
    armas_evento = recursos_usados.get('armas', {})

    # 1. Mazmorra valida
    if mazmorra not in recursos.recursos['mazmorras']:
        return False, "Mazmorra inexistente"

    if not recursos.recursos['mazmorras'][mazmorra]['disponible']:
        return False, "Mazmorra ocupada"

    # 2. Aventureros
    if not aventureros_evento:
        return False, "Debe haber al menos un aventurero"

    # 3. Armas
    if not armas_evento:
        return False, "Los aventureros no pueden ir sin armas"

    if len(armas_evento) < len(aventureros_evento):
        return False, "Cada aventurero debe tener un arma"

    # 4. Compatibilidad aventurero - arma
    ok, msg = restricciones.validar_compatibilidad_aventurero_arma(recursos_usados)
    if not ok:
        return False, msg

    # 5. Co-dependencia
    ok, msg = restricciones.validar_codependencia(recursos_usados)
    if not ok:
        return False, msg

    # 6. Disponibilidad de recursos
    for nombre, cant in aventureros_evento.items():
        disponible = recursos.recursos['aventureros'].get(nombre, {}).get('cantidad', 0)
        if disponible <= 0:
            return False, f"No hay suficientes {nombre}s disponibles"

    for nombre, cant in armas_evento.items():
        disponible = recursos.recursos['armas'].get(nombre, {}).get('cantidad', 0)
        if disponible <= 0:
            return False, f"No hay suficientes {nombre}s disponibles"

    # 7. Duracion
    if duracion_horas <= 0:
        return False, "Duración inválida"

    return True, "Evento válido"
