"""
    events.py

    Diccionario de eventos apuntando a su respectiva función.

    Para agregar una nueva funcionalidad, se debe crear una función que haga lo pertinente y luego
    agregar esa función al diccionario events = {}

"""

# IMPORTS #########################################################################################
import negocio.montecarlo
import json
###################################################################################################


# Funciones
# -------------------------------------------------------------------------------------------------
def ws_test(parameters):
    """
        Retorna un "OK", esta definición de evento es redundante, es solo para ilustrar
    """
    return "OK"

def calcular_montecarlo(parameters):
    """
        Recive una lista de parametros [lleven_menos_de, cantidad_proyectos, mostrar_desde, mostrar_hasta]

        Retorna la siguiente tupla (resultado, tabla, ultima_fila_montecarlo)
        resultado es un float [0.0, 100.0]
        tabla es un array
        ultima_fila_montecarlo es un vector
    """

    menos_de = parameters[0]
    cantidad = parameters[1]
    desde = parameters[2]
    hasta = parameters[3]

    resultados = negocio.montecarlo.calcular(menos_de, cantidad, desde, hasta)

    return str(resultados)

# Diccionario de eventos
# -------------------------------------------------------------------------------------------------
dictionary = {
    "ws-test": ws_test,
    "calcular_montecarlo": calcular_montecarlo,
}


#hola
