# ===========================================
#    VERIFICACION DEL GREMIO - VALIDACION
# ===========================================

# validacion.py
# Verifica si los eventos pueden exitir en el sistema
# Guardian del sitema 

import restricciones

def validar_evento(evento: dict, recursos: dict):

    aventureros_evento = evento.get('aventureros', {})
    armas_evento = evento.get('armas', {})
    mazmorra = evento.get('mazmorra')

    # Compatibilidad aventurero - arma
    ok, msg = restricciones.validar_compatibilidad_aventurero_arma(
        aventureros_evento,
        armas_evento
    )
    if not ok:
        return False, msg

    # Co-dependencia
    ok, msg = restricciones.validar_codependencia(
        aventureros_evento,
        armas_evento
    )
    if not ok:
        return False, msg

    # Recursos disponibles
    for aventurero, cant in aventureros_evento.items():
        if recursos['aventureros'][aventurero]['cantidad'] < cant:
            return False, f"No hay suficientes {aventurero}s disponibles"

    for arma, cant in armas_evento.items():
        if recursos['armas'][arma]['cantidad'] < cant:
            return False, f"No hay suficientes {arma}s disponibles"

    # Mazmorra válida y libre
    if mazmorra not in recursos['mazmorras']:
        return False, "Mazmorra inexistente"

    if not recursos['mazmorras'][mazmorra]['disponible']:
        return False, "Mazmorra ocupada"

    return True, "Evento válido"