"""
    server.py

    Servidor websocket para servir la api al cliente en el navegador
"""

# IMPORTS #########################################################################################
import asyncio
import websockets
import demjson
import json
import events
###################################################################################################


async def server(websocket, path):
    """
        Función que define al servidor websocket
    """

    # Loop principal para mantener la conexión
    while(True):
        # Se recibe el evento
        json_event = await websocket.recv()
        print("[EVENT] Incoming")

        # Transforma objeto json a diccionario python
        event = demjson.decode(json_event)

        # Extraer información del evento
        event_name = str(event["event_name"])
        event_parameters = event["parameters"]

        print("[EVENT NAME] ", event_name)
        print("[EVENT PARAMETERS] ", str(event_parameters))

        # Buscar
        if event_name in events.dictionary:
            result = events.dictionary[event_name](event_parameters)

            # Codificar resultado a json
            encoded_result = json.dumps(result)

            # Enviar respuesta al cliente
            await websocket.send(encoded_result)
        else:
            raise Exception("[ERROR] el evento recibido no existe en el diccionario de eventos")

def run():
    """
        Iniciar el servidor en localhost:8080
    """
    print("Iniciando servidor...")

    start_server = websockets.serve(server, "localhost", 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


run() # <- solo para testear, borrar o se ejecutará automaticamente al importar en __main__.py
