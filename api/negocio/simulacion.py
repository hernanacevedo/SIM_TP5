"""
    simulacion.py
"""

# IMPORTS #########################################################################################
import random
import time
import json
import copy
###################################################################################################


def comparar_horas(hora_1, hora_2):
    """"""
    hora_1 = hora_1.split(":")
    hora_2 = hora_2.split(":")

    if int(hora_1[0]) < int(hora_2[0]):
        return "menor"
    elif int(hora_1[0]) == int(hora_2[0]):
        if int(hora_1[1]) < int(hora_2[1]):
            return "menor"
        elif int(hora_1[1]) == int(hora_2[1]):
            if int(hora_1[2]) < int(hora_2[2]):
                return "menor"
            elif int(hora_1[2]) == int(hora_2[2]):
                return "igual"
            else:
                return "mayor"
        else:
            return "mayor"
    else:
        return "mayor"


def obtener_proximo_evento(experimento):
    """"""
    t_llegada_auto = experimento["llegada_auto"]["proxima_llegada"]
    t_cambio_de_semaforo = experimento["inicio_verde"]["fin_amarillo"]

    # Si no se simulo un tiempo para el evento, se le da un numero ridiculamente grade para siempre elegir el otro
    if t_llegada_auto == "":
        t_llegada_auto = "100:100:100"
    if t_cambio_de_semaforo == "":
        t_cambio_de_semaforo = "100:100:100"

    # Detectar si se debe pasar a un nuevo dia
    if comparar_horas(t_llegada_auto, "10:00:00") == "mayor" and \
            comparar_horas(t_cambio_de_semaforo, "10:00:00") == "mayor":
        experimento["eventos"]["dia"] += 1
        experimento["llegada_auto"]["proxima_llegada"] = restar_horas(t_llegada_auto, "02:00:00")
        experimento["inicio_verde"]["fin_amarillo"] = restar_horas(t_cambio_de_semaforo, "02:00:00")
        experimento["eventos"]["hora"] = "08:00:00"

        e, t = obtener_proximo_evento(experimento)
        return e, t

    e = "llegada_auto"
    t = t_llegada_auto
    if comparar_horas(t_llegada_auto, t_cambio_de_semaforo) == "menor":
        e = "llegada_auto"
    elif comparar_horas(t_llegada_auto, t_cambio_de_semaforo) == "mayor":
        e = "inicio_verde"
        t = t_cambio_de_semaforo
    elif comparar_horas(t_llegada_auto, t_cambio_de_semaforo) == "igual":
        e = "inicio_verde"
        t = t_cambio_de_semaforo

    return e, t


def sumar_hora(hora_1, hora_2):
    hora_1 = hora_1.split(":")
    hora_1 = [int(hora_1[0]), int(hora_1[1]), int(hora_1[2])]
    hora_2 = hora_2.split(":")
    hora_2 = [int(hora_2[0]), int(hora_2[1]), int(hora_2[2])]

    s = hora_1[2] + hora_2[2]
    m = hora_1[1] + hora_2[1] + s//60
    h = hora_1[0] + hora_2[0] + m//60

    hora_1 = [h, m % 60, s % 60]

    # Se vuelve a transformar la hora en un string
    hora = str(hora_1[0])+":"+str(hora_1[1])+":"+str(hora_1[2])

    return hora


def restar_horas(hora_1, hora_2):
    """"""
    hora_1 = hora_1.split(":")
    hora_1 = [int(hora_1[0]), int(hora_1[1]), int(hora_1[2])]
    hora_2 = hora_2.split(":")
    hora_2 = [int(hora_2[0]), int(hora_2[1]), int(hora_2[2])]

    s = hora_1[2] + ~hora_2[2] + 1
    m = hora_1[1] + ~hora_2[1] + s//60 + 1
    h = hora_1[0] + ~hora_2[0] + m//60 + 1


    hora_1 = [h, m % 60, s % 60]

    # Se vuelve a transformar la hora en un string
    hora = str(hora_1[0])+":"+str(hora_1[1])+":"+str(hora_1[2])

    return hora


def simular_inicio_verde(experimento):
    """"""
    # Calcular el max por pasada
    if experimento["ac_pasada"] > experimento["q_max_en_una_pasada"]:
        experimento["q_max_en_una_pasada"] = experimento["ac_pasada"]
    experimento["ac_pasada"] = 0

    # Obtener el semaforo que se ha puesto en verde
    semaforo = experimento["inicio_verde"]["proximo"][-1]

    # Obtener la duración del semaforo
    if semaforo == "1":
        duracion_verde = 20
    else:
        duracion_verde = 40

    hora_actual = experimento["eventos"]["hora"]
    fin_verde = sumar_hora(hora_actual, "00:00:"+str(duracion_verde))
    fin_amarillo = sumar_hora(fin_verde, "00:00:10")

    experimento["inicio_verde"]["fin_verde"] = fin_verde
    experimento["inicio_verde"]["fin_amarillo"] = fin_amarillo

    # Calcular el proximo semaforo a ponerse en verde
    proximo_semaforo = "s2"
    if experimento["inicio_verde"]["proximo"] == "s2":
        proximo_semaforo = "s1"
    experimento["inicio_verde"]["proximo"] = proximo_semaforo

    return experimento


def completar_simulacion(experimento):
    """"""
    # Actualizar estado de los semaforos
    proximo = experimento["inicio_verde"]["proximo"]
    if proximo == "s1":
        actual = "s2"
    else:
        actual = "s1"

    hora_actual = experimento["eventos"]["hora"]

    fin_verde = experimento["inicio_verde"]["fin_verde"]
    fin_amarillo = experimento["inicio_verde"]["fin_amarillo"]

    experimento["semaforos"]["s1"]["estado"] = "habilitado"
    experimento["semaforos"]["s1"]["color"] = "verde"
    experimento["semaforos"]["s2"]["estado"] = "habilitado"
    experimento["semaforos"]["s2"]["color"] = "verde"

    if comparar_horas(hora_actual, fin_verde) == "mayor":
        experimento["semaforos"][actual]["estado"] = "inhabilitado"
        experimento["semaforos"][actual]["color"] = "amarillo"

    experimento["semaforos"][proximo]["estado"] = "inhabilitaado"
    experimento["semaforos"][proximo]["color"] = "rojo"

    return experimento


def obtener_proxima_llegada(rnd, calle, hora):
    """"""

    return "00:00:15"


def obtener_semaforo(rnd):
    """"""
    p_colon = 0.5
    p_urquiza = 0.1

    if rnd > p_colon:
        return "s2"
    else:
        return "s1"


def simular_llegada_auto(experimento):
    """"""
    hora = experimento["eventos"]["hora"]
    rnd = random.random()
    semaforo = obtener_semaforo(rnd)
    tiempo_entre_llegadas = obtener_proxima_llegada(rnd, semaforo, hora)
    proxima_llegada = sumar_hora(hora, tiempo_entre_llegadas)

    experimento["llegada_auto"]["proxima_llegada"] = proxima_llegada

    # Se agrega el auto que llegó a la cola, si no tiene que esperar, se lo va a hacer pasar y en el vector final a
    # mostrar, no se habrá incrementado la cola
    experimento["semaforos"][semaforo]["cola"] += 1

    # Agregar el objeto a la lista de objetos
    calles = {"s1": "colon", "s2": "urquiza"}
    auto = {
        "estado": "E", "calle": calles[semaforo], "inicio_espera": hora
    }
    experimento["autos"].append(auto)

    return experimento


def hay_cruce(experimento):
    """"""
    cola_s1 = experimento["semaforos"]["s1"]["cola"]
    cola_s2 = experimento["semaforos"]["s2"]["cola"]
    estado_s1 = experimento["semaforos"]["s1"]["estado"]
    estado_s2 = experimento["semaforos"]["s2"]["estado"]

    hora_actual = experimento["eventos"]["hora"]
    fin_cruce = experimento["cruce"]["fin_cruce"]
    if fin_cruce != "":
        if not(comparar_horas(hora_actual, fin_cruce) == "mayor"):
            return False

    if cola_s1 > 0 and estado_s1 == "habilitado":
        return "s1"
    elif cola_s2 > 0 and estado_s2 == "inhabilitado":
        return "s2"
    else:
        return False


def simular_cruce(experimento, semaforo):
    rnd = random.random()
    tiempo = "00:00:2" # -> esto debe calcularse
    fin_cruce = sumar_hora(experimento["eventos"]["hora"], tiempo)

    experimento["cruce"]["rnd"] = rnd
    experimento["cruce"]["tiempo"] = tiempo
    experimento["cruce"]["fin_cruce"] = fin_cruce

    # Detectar si hay infraccion
    if comparar_horas(fin_cruce, experimento["inicio_verde"]["fin_amarillo"]) == "mayor":
        experimento["infraccion"] = "si"
        experimento["ac_infracciones"] += 1

    # Determinar cantidad de autos a cruzar
    cola = experimento["semaforos"][semaforo]["cola"]
    if cola >= 3:
        q = 3
    else:
        q = cola

    # Decrementar la cola de autos
    experimento["semaforos"][semaforo]["cola"] -= q

    # Actualizar estados
    for i in range(q - 1):
        experimento["autos"][i]["estado"] = "P"
        espera = restar_horas(experimento["eventos"]["hora"], experimento["autos"][i]["inicio_espera"])

        experimento["ac_espera"] = sumar_hora(experimento["ac_espera"], espera)

        if comparar_horas(experimento["eventos"]["hora"], experimento["autos"][i]["inicio_espera"]) == "mayor":
            experimento["q_max_en_espera"] += 1

    if semaforo == "s1":
        experimento["q_autos_por_colon"] += q

    experimento["ac_pasada"] += q

    return experimento


def limpiar_objetos(experimento):
    """
        Es una cola, siempre se van a ir los primeros, ommitir al primer E
    """
    for i in range(len(experimento["autos"])):
        if experimento["autos"][0]["estado"] == "P":
            experimento["autos"].pop(0)
        else:
            break

    return experimento


def completar_linea(experimento):
    """"""
    linea = copy.deepcopy(experimento)
    l = len(linea["autos"])
    if l < 6:
        for i in range(6-l):
            linea["autos"].append({"estado": "", "calle": "", "inicio_espera": ""})

    return linea

def simular(dias, j, k):
    """
    """

    # Iniciar el vector(dict) de simulacion
    experimento = {
        "eventos": {
            "evento": "", "hora": "8:00:00", "dia": 1
        },
        "llegada_auto": {
            "rnd_calle": "", "calle": "", "rnd_tiempo": "", "proxima_llegada": ""
        },
        "inicio_verde": {
            "fin_verde": "", "fin_amarillo": "08:00:00", "proximo": "s1"
        },
        "cruce": {
            "rnd": "", "tiempo": "", "fin_cruce": ""
        },
        "semaforos": {
            "s1": {"estado": "habilitado", "color": "rojo", "cola": 0},
            "s2": {"estado": "inhabilitado", "color": "rojo", "cola": 0},
        },
        "infraccion": "",
        "ac_infracciones": 0,
        "ac_espera": "00:00:00",
        "q_autos_por_colon": 0,
        "q_max_en_espera": 0,
        "ac_pasada": 0,
        "q_max_en_una_pasada": 0,
        "autos": []
    }

    simular_evento = {
        "inicio_verde": simular_inicio_verde,
        "llegada_auto": simular_llegada_auto
    }

    tabla = []

    experimento = simular_evento["llegada_auto"](experimento)

    contador = 0
    while comparar_horas(experimento["eventos"]["hora"], "10:00:00") != "mayor":
        # Buscar evento actual, sino habilitar un semaforo
        e, t = obtener_proximo_evento(experimento)

        experimento["eventos"]["evento"] = e

        # Borrar autos que ya han pasado
        experimento = limpiar_objetos(experimento)

        # Simular evento y actualizar vector
        experimento["eventos"]["hora"] = t
        experimento = simular_evento[e](experimento)

        # Simular el resto del vector y actulizar
        experimento = completar_simulacion(experimento)

        # Si hay cruce, simular
        if hay_cruce(experimento):
            simular_cruce(experimento, hay_cruce(experimento))

        # Guardar vector si se encuentra dentro del rango
        if j <= contador <= k:
            linea = completar_linea(experimento)
            tabla.append(copy.deepcopy(linea))

        contador += 1
        if int(experimento["eventos"]["dia"]) > int(dias):
            break

        completado = (experimento["eventos"]["dia"]/dias)*100
        print("COMPLETADO:", round(completado), "%")


    return tabla

