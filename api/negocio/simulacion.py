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
    t_fin_cruce = experimento["cruce"]["fin_cruce"]

    # Si no se simulo un tiempo para el evento, se le da un numero ridiculamente grade para siempre elegir el otro
    if t_llegada_auto == "":
        t_llegada_auto = "100:100:100"
    if t_cambio_de_semaforo == "":
        t_cambio_de_semaforo = "100:100:100"
    if t_fin_cruce == "":
        t_fin_cruce = "100:100:100"

    # Detectar si se debe pasar a un nuevo dia
    if comparar_horas(t_llegada_auto, "10:00:00") == "mayor" and \
            comparar_horas(t_cambio_de_semaforo, "10:00:00") == "mayor":
        experimento["eventos"]["dia"] += 1
        experimento["llegada_auto"]["proxima_llegada"] = restar_horas(t_llegada_auto, "02:00:00")
        experimento["inicio_verde"]["fin_amarillo"] = restar_horas(t_cambio_de_semaforo, "02:00:00")
        experimento["cruce"]["fin_cruce"] = restar_horas(t_fin_cruce, "02:00:00")
        experimento["eventos"]["hora"] = "08:00:00"

        e, t = obtener_proximo_evento(experimento)
        return e, t

    e = "llegada_auto"
    t = t_llegada_auto
    if comparar_horas(t_llegada_auto, t_cambio_de_semaforo) == "menor"\
                and comparar_horas(t_llegada_auto, t_fin_cruce) == "menor":
        e = "llegada_auto"
        t = t_llegada_auto
    elif comparar_horas(t_cambio_de_semaforo, t_fin_cruce) == "menor"\
                and comparar_horas(t_cambio_de_semaforo, t_llegada_auto) == "menor":
        e = "inicio_verde"
        t = t_cambio_de_semaforo
    elif t_fin_cruce != "100:100:100":
        e = "fin_cruce"
        t = t_fin_cruce

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

    experimento["semaforos"][proximo]["estado"] = "inhabilitado"
    experimento["semaforos"][proximo]["color"] = "rojo"

    return experimento


def generarDistribucionNormal(media, desviacion):
        Z=round(
            (
            (
                (random.random()+random.random()+random.random()+random.random()+ random.random()+random.random()+
                random.random()+random.random()+random.random()+random.random()+random.random()+random.random())
            - 6 ) * desviacion) + media
        , 1)

        return abs(Z)



def obtener_proxima_llegada(semaforo, hora):
    """"""
    calle = int(semaforo[-1])
    horaActual = hora.split(":")
    horaActual = int(horaActual[0])

    if calle == 2 and horaActual >= 8 and horaActual <= 10:
        tiempo_entre_lleg = generarDistribucionNormal(1, 1)

    elif calle == 1 and horaActual >= 8 and horaActual < 9:
        tiempo_entre_lleg = generarDistribucionNormal(3, 1)

    else:
        tiempo_entre_lleg = generarDistribucionNormal(2, 0.5)

    tiempo = "00:00:"+str(int(tiempo_entre_lleg))

    return tiempo_entre_lleg, tiempo


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
    rnd_c = random.random()
    semaforo = obtener_semaforo(rnd_c)

    rnd_t, tiempo_entre_llegadas = obtener_proxima_llegada(semaforo, hora)
    proxima_llegada = sumar_hora(hora, tiempo_entre_llegadas)

    experimento["llegada_auto"]["proxima_llegada"] = proxima_llegada

    experimento["llegada_auto"]["rnd_calle"] = round(rnd_c, 2)
    experimento["llegada_auto"]["rnd_tiempo"] = round(rnd_t, 2)

    # Se agrega el auto que llegó a la cola, si no tiene que esperar, se lo va a hacer pasar y en el vector final a
    # mostrar, no se habrá incrementado la cola
    experimento["semaforos"][semaforo]["cola"] += 1

    # Agregar el objeto a la lista de objetos
    calles = {"s1": "colon", "s2": "urquiza"}
    auto = {
        "estado": "E", "calle": calles[semaforo], "inicio_espera": hora
    }
    experimento["autos"].append(auto)

    experimento["llegada_auto"]["calle"] = calles[semaforo]

    experimento["ac_autos"] += 1

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
    elif cola_s2 > 0 and estado_s2 == "habilitado":
        return "s2"
    else:
        return False


def obtener_tiempo_cruce(semaforo):
    """"""
    calle = int(semaforo[-1])

    if calle == 1:
        tiempo_entre_lleg= generarDistribucionNormal(4, 1)

    else:
        tiempo_entre_lleg = generarDistribucionNormal(3, 0.5)

    tiempo = "00:00:"+str(int(tiempo_entre_lleg))

    return tiempo_entre_lleg, tiempo


def simular_cruce(experimento, semaforo):
    rnd, tiempo = obtener_tiempo_cruce(semaforo)
    fin_cruce = sumar_hora(experimento["eventos"]["hora"], tiempo)

    experimento["cruce"]["rnd"] = rnd
    experimento["cruce"]["tiempo"] = tiempo
    experimento["cruce"]["fin_cruce"] = fin_cruce

    # Detectar si hay infraccion
    if comparar_horas(fin_cruce, experimento["inicio_verde"]["fin_amarillo"]) == "mayor":
        experimento["infraccion"] = "si"
        experimento["ac_infracciones"] += 1
    else:
        experimento["infraccion"] = ""

    if semaforo == 1:
        m = 3
    else:
        m = 4

    # Determinar cantidad de autos a cruzar
    cola = experimento["semaforos"][semaforo]["cola"]
    if cola >= m:
        q = m
    else:
        q = cola

    # Decrementar la cola de autos
    experimento["semaforos"][semaforo]["cola"] -= q

    # Actualizar estados
    for i in range(q - 1):
        experimento["autos"][i]["estado"] = "P"
        espera = restar_horas(experimento["eventos"]["hora"], experimento["autos"][i]["inicio_espera"])

        experimento["ac_espera"] = sumar_hora(experimento["ac_espera"], espera)
        experimento["ac_espera"] = sumar_hora(experimento["ac_espera"], tiempo)

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


def limpiar_experimento(experimento):
    """"""
    experimento["cruce"]["rnd"] = ""
    experimento["cruce"]["tiempo"] = ""
    experimento["cruce"]["fin_cruce"] = ""

    return experimento


def calcular_promedio_espera(experimento):
    """"""
    ac_espera = experimento["ac_espera"]

    # Transformar a segundos
    ac_espera = ac_espera.split(":")
    h = int(ac_espera[0])
    m = int(ac_espera[1])
    s = int(ac_espera[2])
    ac_espera = h*60*60 + m*60 + s

    n = int(ac_espera/experimento["ac_autos"])

    # Transformar nuevamente a formato hora
    s = n % 60
    m = n // 60
    m = m % 60
    h = n // (60*60)
    h = h % (60*60)

    tiempo = str(h)+":"+str(m)+":"+str(s)

    return tiempo


def simular_fin_cruce(experimento):
    """"""
    experimento["cruce"]["rnd"] = ""
    experimento["cruce"]["tiempo"] = ""
    experimento["cruce"]["fin_cruce"] = ""

    return experimento

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
        "ac_autos": 0,
        "autos": []
    }

    simular_evento = {
        "inicio_verde": simular_inicio_verde,
        "llegada_auto": simular_llegada_auto,
        "fin_cruce": simular_fin_cruce
    }

    tabla = []

    experimento = simular_evento["llegada_auto"](experimento)

    completado = 0
    contador = 0
    while comparar_horas(experimento["eventos"]["hora"], "10:00:00") != "mayor":
        # Buscar evento actual, sino habilitar un semaforo
        e, t = obtener_proximo_evento(experimento)

        experimento["eventos"]["evento"] = e

        # Borrar autos que ya han pasado
        experimento = limpiar_objetos(experimento)

        # Restablecer valores no necesarios del vector
        #experimento = limpiar_experimento(experimento)

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

        if round((experimento["eventos"]["dia"]/dias)*100) > completado:
            print("COMPLETADO:", round(completado), "%")
        completado = round((experimento["eventos"]["dia"]/dias)*100)

    print(round(completado))

    # Agregar ultima fila
    linea = completar_linea(experimento)
    tabla.append(copy.deepcopy(linea))

    promedio = calcular_promedio_espera(experimento)

    resultados = {
        "promedio": promedio,
        "filas": contador
    }

    resultado = [resultados, tabla]

    return resultado

