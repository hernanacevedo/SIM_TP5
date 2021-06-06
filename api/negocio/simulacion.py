"""
    simulacion.py
"""

# IMPORTS #########################################################################################

###################################################################################################




def simulate_line():
    """
    """
    pass


def simular_dia():
    """
    """
    # Iniciar el vector(dict) de simulacion
    experimento = {
        "eventos": {
            "evento": "", "hora": "8:00:00", "dia": 0
        },
        "llegada_auto": {
            "rnd_calle": "", "calle": "", "rnd_tiempo": "", "proxima_llegada": ""
        },
        "cambio_de_semaforo": [8, 0, 0],
        "fin_verde": {
            "s1": {"ini": "", "fin": ""}, "s2": {"ini": "", "fin": ""}
        },
        "fin_amarillo": {
            "s1": "", "s2": ""
        },
        "tiempo_de_cruce": {
            "s1": {"rnd": "", "tiempo": "", "fin": ""},
            "s2": {"rnd": "", "tiempo": "", "fin": ""}
        },
        "semaforos": {
            "s1": {"estado": "habilitado", "color": "rojo", "cola": 0},
            "s2": {"estado": "inhabilitado", "color": "rojo", "cola": 0},
        },
        "multa": "",
        "ac_tiempo_de_permanencia": 0,
        "q_autos_por_colon": 0,
        "q_max_en_espera": 0,
        "q_max_en_una_pasada": 0
    }

    while experimento["eventos"]["hora"] <= "10:00:00":
        pass
        # Buscar evento actual, sino habilitar un semaforo

        # Simular evento y actualizar vector

        # Simular el resto del vector y actulizar

        # Guardar vector si se encuentra dentro del rango



