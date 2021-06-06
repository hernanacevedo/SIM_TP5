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

        // calcular_montecarlo
        if(event.data != "OK") {
            console.log(event.data);
            // Obtener datos
            var data = JSON.parse(event.data);
            //console.log(data);

            var result = data[0].toFixed(2);
            var tabla = data[1];

            // Resetear la tabla
            empty_table = `<table id="result_table">
                 <tr id="table_header">
                     <th rowspan="2">n Proyecto</th>
                     <th colspan="2">A</th>
                     <th colspan="2">B</th>
                     <th colspan="2">C</th>
                     <th colspan="2">D</th>
                     <th colspan="3" id="result_tag">Resultado: -</th>
                 </tr>
                 <tr>
                     <th>RND</th>
                     <th>Semana</th>
                     <th>RND</th>
                     <th>Semana</th>
                     <th>RND</th>
                     <th>Semana</th>
                     <th>RND</th>
                     <th>Semana</th>

                     <th>Total</th>
                     <th>Exito</th>
                     <th>Exitos acumulados</th>
                 </tr>
            </table>`
            $("#result_table").html(empty_table);

            $("#result_tag").text("Resultado: "+result+"%");

            // Dibujar tabla
            var i;
            for(i=0; i<tabla.length; i++) {
                row_data = tabla[i];

                // Traducir exitos de 0,1 a NO,SI
                if (row_data[10] == 0){
                    row_data[10] = "NO"
                } else {
                    row_data[10] = "SI"
                }

                new_row = `<tr>
                         <td>${row_data[0]}</td>
                         <td>${row_data[1]}</td>
                         <td>${row_data[2]}</td>
                         <td>${row_data[3]}</td>
                         <td>${row_data[4]}</td>
                         <td>${row_data[5]}</td>
                         <td>${row_data[6]}</td>
                         <td>${row_data[7]}</td>
                         <td>${row_data[8]}</td>
                         <td>${row_data[9]}</td>
                         <td>${row_data[10]}</td>
                         <td>${row_data[11]}</td>
                </tr>`;
                $("#result_table").append(new_row);

                // Destacar ultima linea
                if(i == tabla.length - 2) {
                    html = '<tr><td colspan="12" id="last_line">-- ULTIMA LINEA --</td></tr>'
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

    // Caclular montecarlo
    $("#calculate").click(function() {
        console.log("[CALCULAR] Calcular montecarlo");

        menos_de = Number($("#inp_restriction").val());
        cantidad = Number($("#inp_N").val());
        desde = Number($("#inp_i").val());
        hasta = Number($("#inp_j").val());

        parameters = [menos_de, cantidad, desde, hasta];
        event = `{"event_name": "calcular_montecarlo", "parameters": [${menos_de}, ${cantidad}, ${desde}, ${hasta}]}`;
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
        if($("#inp_restriction").val() <= 0) {
            $("#inp_restriction").css({"border-color":"red"});
        } else {
            $("#inp_restriction").css({"border-color":"gray"});
        }
        if($("#inp_N").val() <= 0) {
            $("#inp_N").css({"border-color":"red"});
        } else {
            $("#inp_N").css({"border-color":"gray"});
        }
        if($("#inp_i").val() <= 0 || $("#inp_i").val() > $("#inp_N").val() - 1) {
            $("#inp_i").css({"border-color":"red"});
        } else {
            $("#inp_i").css({"border-color":"gray"});
        }
        var dif = $("#inp_j").val() - $("#inp_i").val();
        var i = $("#inp_i").val();
        var j = $("#inp_j").val();
        var N = $("#inp_N").val();

        if(j <= 0 || dif < 0 || j > N) {
            $("#inp_j").css({"border-color":"red"});
        } else {
            $("#inp_j").css({"border-color":"gray"});
        }
    });

});
