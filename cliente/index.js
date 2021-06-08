/*
    index.js

    Lógica para el cliente

    !IMPORTANTE! todos los eventos que se envian se deben enviar en un vector donde la posición
    cero corresponde al nombre del evento, el siguiente debe contener una tupla de parametros
    o ser inexistente
    ["nombre_evento", (param1, param2, param3, paramN)]
*/


// Se carga el script
$(document).ready(function(){
    // Para chequear por consola que el script se ejecutó
    console.log("Hola Mundo")

    let socket = new WebSocket("ws://localhost:8080");

    // Función para mostrar mensaje de conectado
    function show_connected() {
        // Informar por consola la conexión exitosa
        console.log("Conectado ");
        // Cambiar el estado de conexión a "conectado"
        $("#conn_state").text("conectado");
        $("#conn_state").css({
            "color":"green",
        });
        // Desvanecer y transformar en boton de chequear conexión
        $("#conn_state").fadeIn(1500, function(){
            $("#conn_state").fadeOut(1500);
        });
    }

    function show_disconnected() {
        // Informar por consola la falla en la conexión
        console.log("Problema de conexión, reconectando...");

        // Cambiar el estado de conexión a "reconectando..."
        $("#conn_state").text("reconectando...");
        $("#conn_state").css({
            "color":"red",
        });
        $("#conn_state").fadeIn(1500);
    }

    // Cuando se conecta al servidor webscocket
    socket.onopen = function(e) {
        show_connected();
    }

    // Cuando se pierde la conexión al servidor websocket
    socket.onclose = function(e) {
        show_disconnected();
    }


    // Manejo de eventos
    socket.onmessage = function(event) {

        // ws-test
        if(event.data == "OK") {
            show_connected();
        }

        // calcular_simulacion
        if(event.data != "OK") {
            // Obtener datos
            var data = JSON.parse(event.data);
            //data = JSON.stringify(data)

            //var result = data[0].toFixed(2);
            var tabla = data[1];
            var resultados = data[0]
            console.log(event.data);

            // Resetear la tabla
            empty_table = `<table id="result_table">
             <tr id="table_header">
                 <th colspan="3" rowspan="1">Promedio permanencia: ${resultados.promedio}</th>
                 <th colspan="4" rowspan="1">Filas simuladas: ${resultados.filas}</th>
                 <th colspan="3" rowspan="2">inicio_verde</th>
                 <th colspan="3" rowspan="2">Cruce</th>
                 <th colspan="1" rowspan="3">Infraccion</th>
                 <th colspan="1" rowspan="3">Ac infracciones</th>
                 <th colspan="1" rowspan="3">Cantidad que pasaron por Colon</th>
                 <th colspan="1" rowspan="3">Cantidad max que tuvieron que esperar</th>
                 <th colspan="1" rowspan="3">Ac de pasadas</th>
                 <th colspan="1" rowspan="3">Cantidad max que cruzaron en una pasada</th>
                 <th colspan="1" rowspan="3">Ac autos</th>
                 <th colspan="6" rowspan="1">Semaforos</th>
                 <th colspan="18" rowspan="1">Autos</th>
             </tr>
             <tr>
                <th colspan="3" rowspan="1">Eventos</th>
                <th colspan="4" rowspan="1">llegada_auto</th>
                <th colspan="3" rowspan="1">S1(Colón)</th>
                 <th colspan="3" rowspan="1">S2(Urquiza)</th>
                 <th colspan="3" rowspan="1">Auto 1</th>
                 <th colspan="3" rowspan="1">Auto 2</th>
                 <th colspan="3" rowspan="1">Auto 3</th>
                 <th colspan="3" rowspan="1">Auto 4</th>
                 <th colspan="3" rowspan="1">Auto 5</th>
                 <th colspan="3" rowspan="1">Auto N</th>

             </tr>
             <tr>

                <th>Evento</th>
                 <th>Hora</th>
                 <th>Dia</th>

                 <th>RND</th>
                 <th>Calle</th>
                 <th>RND</th>
                 <th>Proxima llegada</th>

                 <th>Fin_verde</th>
                 <th>Fin_amarillo</th>
                 <th>Proximo</th>

                 <th>RND</th>
                 <th>Tiempo</th>
                 <th>Fin cruce</th>

                 <th>Estado</th>
                 <th>Color</th>
                 <th>Cola</th>

                 <th>Estado</th>
                 <th>Color</th>
                 <th>Cola</th>

                 <th>Estado</th>
                 <th>Calle</th>
                 <th>Inicio espera</th>

                 <th>Estado</th>
                 <th>Calle</th>
                 <th>Inicio espera</th>

                 <th>Estado</th>
                 <th>Calle</th>
                 <th>Inicio espera</th>

                 <th>Estado</th>
                 <th>Calle</th>
                 <th>Inicio espera</th>

                 <th>Estado</th>
                 <th>Calle</th>
                 <th>Inicio espera</th>

                 <th>Estado</th>
                 <th>Calle</th>
                 <th>Inicio espera</th>


             </tr>
        </table>`
            $("#result_table").html(empty_table);

            //$("#result_tag").text("Resultado: "+result+"%");

            // Dibujar tabla
            var i;
            for(i=0; i<tabla.length; i++) {
                row_data = tabla[i];

                console.log(row_data.autos)

                new_row = `<tr>
                         <td>${row_data.eventos.evento}</td>
                         <td>${row_data.eventos.hora}</td>
                         <td>${String(row_data.eventos.dia)}</td>
                         <td>${row_data.llegada_auto.rnd_calle}</td>
                         <td>${row_data.llegada_auto.calle}</td>
                         <td>${row_data.llegada_auto.rnd_tiempo}</td>
                         <td>${row_data.llegada_auto.proxima_llegada}</td>
                         <td>${row_data.inicio_verde.fin_verde}</td>
                         <td>${row_data.inicio_verde.fin_amarillo}</td>
                         <td>${row_data.inicio_verde.proximo}</td>
                         <td>${row_data.cruce.rnd}</td>
                         <td>${row_data.cruce.tiempo}</td>
                         <td>${row_data.cruce.fin_cruce}</td>
                         <td>${row_data.infraccion}</td>
                         <td>${row_data.ac_infracciones}</td>
                         <td>${row_data.q_autos_por_colon}</td>
                         <td>${row_data.q_max_en_espera}</td>
                         <td>${row_data.ac_pasada}</td>
                         <td>${row_data.q_max_en_una_pasada}</td>
                         <td >${row_data.ac_autos}</td>
                         <td>${row_data.semaforos.s1.estado}</td>
                         <td>${row_data.semaforos.s1.color}</td>
                         <td>${row_data.semaforos.s1.cola}</td>
                         <td>${row_data.semaforos.s2.estado}</td>
                         <td>${row_data.semaforos.s2.color}</td>
                         <td>${row_data.semaforos.s2.cola}</td>

                         <td>${row_data.autos[0].estado}</td>
                         <td>${row_data.autos[0].calle}</td>
                         <td>${row_data.autos[0].inicio_espera}</td>

                         <td>${row_data.autos[1].estado}</td>
                         <td>${row_data.autos[1].calle}</td>
                         <td>${row_data.autos[1].inicio_espera}</td>

                         <td>${row_data.autos[2].estado}</td>
                         <td>${row_data.autos[2].calle}</td>
                         <td>${row_data.autos[2].inicio_espera}</td>

                         <td>${row_data.autos[3].estado}</td>
                         <td>${row_data.autos[3].calle}</td>
                         <td>${row_data.autos[3].inicio_espera}</td>

                         <td>${row_data.autos[4].estado}</td>
                         <td>${row_data.autos[4].calle}</td>
                         <td>${row_data.autos[4].inicio_espera}</td>

                         <td>${row_data.autos[5].estado}</td>
                         <td>${row_data.autos[5].calle}</td>
                         <td>${row_data.autos[5].inicio_espera}</td>

                </tr>`;

                $("#result_table").append(new_row);

                // Destacar ultima linea
                if(i == tabla.length - 2) {
                    html = '<tr><td colspan="45" id="last_line">-- ULTIMA LINEA --</td></tr>'
                    $("#result_table").append(html);
                    $("#last_line").css({"background-color":"green", "color":"white"});
                }
            }

        }

    }

    // Para testear si el servidor ws funciona
    $("#ws_test").click(function() {
        console.log("[TEST] Testeando conexión con el servidor");
        event = `{"event_name": "ws-test", "parameters": []}`
        socket.send(event);
    });

    // Caclular simulacion
    $("#calculate").click(function() {
        console.log("[CALCULAR] Calcular simulacion");

        dias = Number($("#inp_x").val());
        desde = Number($("#inp_i").val());
        hasta = Number($("#inp_j").val());

        parameters = [dias, desde, hasta];
        event = `{"event_name": "simular", "parameters": [${dias}, ${desde}, ${hasta}]}`;
        socket.send(event);
    });




    // Para mostrar la sombra al escrollear
    $(".display").scroll(function(){
        if ($(".display").scrollTop() == 0){
            $(".options").css("box-shadow","0px 10px 15px -8px transparent");
        } else {
            $(".options").css("box-shadow","0px 10px 15px -8px black");
        }
    });

    // Validación en tiempo real de los datos
    $(window).keyup(function() {
        if($("#inp_x").val() <= 0) {
            $("#inp_x").css({"border-color":"red"});
        } else {
            $("#inp_x").css({"border-color":"gray"});
        }

        if($("#inp_i").val() < 0 || $("#inp_i").val() > $("#inp_x").val() - 1) {
            $("#inp_i").css({"border-color":"red"});
        } else {
            $("#inp_i").css({"border-color":"gray"});
        }
        var dif = $("#inp_j").val() - $("#inp_i").val();
        var i = $("#inp_i").val();
        var j = $("#inp_j").val();
        var x = $("#inp_x").val();

        if(j <= 0 || dif < 0) {
            $("#inp_j").css({"border-color":"red"});
        } else {
            $("#inp_j").css({"border-color":"gray"});
        }
    });

});
