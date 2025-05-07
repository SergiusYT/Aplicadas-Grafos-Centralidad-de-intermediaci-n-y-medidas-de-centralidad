let network;
let infectadosPrevios = new Set();

async function cargarGrafo() {
    const data = await eel.obtener_estado()();
    const nodes = new vis.DataSet(data.nodes.map(n => ({
        id: n.id,
        label: n.id,
        color: n.color,
        x: n.x * 500,
        y: n.y * 500,
        fixed: false
    })));
    const edges = new vis.DataSet(data.edges);
    const container = document.getElementById('network');
    const options = { physics: true };
    network = new vis.Network(container, { nodes, edges }, options);

    network.on("dragEnd", function (params) {
        if (params.nodes.length > 0) {
            const id = params.nodes[0];
            const position = network.getPositions([id])[id];
            eel.actualizar_posicion(id, position.x, position.y);
        }
    });

    // ✅ Nuevo evento: al hacer click en un nodo, colocar su id en el input
    network.on("click", function (params) {
        if (params.nodes.length > 0) {
            const id = params.nodes[0];
            document.getElementById('nodoBloquear').value = id;
        }
    });

    
}

function hexToRgb(hex) {
    const bigint = parseInt(hex.replace('#', ''), 16);
    return [ (bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255 ];
}

function rgbToHex(rgb) {
    return '#' + rgb.map(x => x.toString(16).padStart(2, '0')).join('');
}

function interpolateColor(color1, color2, factor) {
    const result = color1.slice();
    for (let i = 0; i < 3; i++) {
        result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
    }
    return result;
}

async function actualizarColores() {
    const data = await eel.obtener_estado()();

    const infectadosNuevos = new Set();
    data.nodes.forEach(n => {
        if (n.color === 'red' && !infectadosPrevios.has(n.id)) {
            infectadosNuevos.add(n.id);
        }

        network.body.data.nodes.update({
            id: n.id,
            color: colorNameToHex(n.color),
        });
    });

    infectadosPrevios = new Set(data.nodes.filter(n => n.color === 'red').map(n => n.id));

    // Activar efecto de resplandor para infectados nuevos
    infectadosNuevos.forEach(id => pulsoNodo(id));
}

function colorNameToHex(name) {
    switch (name) {
        case 'green': return '#00cc00';
        case 'orange': return '#ff9900';
        case 'red': return '#cc0000';
        default: return '#cccccc';
    }
}

function pulsoNodo(id) {
    let size = 30;
    let maxSize = 45;
    let minSize = 30;
    let growing = true;
    let steps = 12;
    let count = 0;

    const interval = setInterval(() => {
        if (!network.body.data.nodes.get(id)) {
            clearInterval(interval);
            return;
        }

        size += growing ? 1.5 : -1.5;

        if (size >= maxSize) growing = false;
        if (size <= minSize) growing = true;

        network.body.data.nodes.update({
            id: id,
            size: size,
            borderWidth: 4,
            borderWidthSelected: 6,
            color: {
                background: '#ff0000',
                border: '#ff5555',
                highlight: {
                    background: '#ff2222',
                    border: '#ffaaaa'
                }
            }
        });

        count++;
        if (count > steps) {
            // Restaurar tamaño original
            network.body.data.nodes.update({
                id: id,
                size: 30,
                borderWidth: 1,
                color: {
                    background: '#cc0000',
                    border: '#660000',
                    highlight: {
                        background: '#cc0000',
                        border: '#ff5555'
                    }
                }
            });
            clearInterval(interval);
        }
    }, 80);
}


async function actualizarEstadisticas() {
    const data = await eel.obtener_estadisticas()();
    document.getElementById('stats').innerHTML = `
        🦠 Infectados: ${data.infectados} <br>
        🔒 Bloqueados: ${data.bloqueados} <br>
        🏆 Puntuación: ${data.puntuacion} <br>
        ⚠️ <b>Advertencias:</b><br>
        ${data.objetivos_infectados.length > 0 ? "❌ Objetivos hackeados: " + data.objetivos_infectados.join(", ") + "<br>" : ""}
        ${data.objetivos_en_peligro.length > 0 ? "⚠️ Objetivos en peligro: " + data.objetivos_en_peligro.join(", ") + "<br>" : ""}
        ${data.objetivos_infectados.length === 0 && data.objetivos_en_peligro.length === 0 ? "✅ Ningún objetivo en peligro actualmente." : ""}
    `;
}


async function mostrarCentralidades() {
    const data = await eel.obtener_centralidades()();
    const tabla = document.getElementById('centralidadesTabla');
    Object.keys(data).forEach(nodo => {
        const fila = document.createElement('tr');
        fila.innerHTML = `<td>${nodo}</td><td>${data[nodo].grado}</td><td>${data[nodo].intermediacion}</td>`;
        tabla.appendChild(fila);
    });
}





let propagacion;  // Se mantiene la referencia de la propagación

async function autoPaso() {
    const nodo = document.getElementById('nodoBloquear').value.toUpperCase();
    const resultado = await eel.siguiente_paso(nodo || null)();
    
    await actualizarColores();  // Solo actualiza los colores

    // Agregar lógica para proteger un nodo
    if (nodo && resultado !== "hackeo" && resultado !== "detenido") {
        proteccionNodo(nodo);
    }

    // Mostrar alertas si ganó o perdió
    if (resultado.startsWith("todos_infectados")) {
        alert("❌ Todos los servidores críticos fueron infectados. ¡Hackeo exitoso!");
        clearInterval(propagacion);
    } else if (resultado.startsWith("detenido")) {
        const objetivosSalvados = resultado.split(":")[1];
        alert("✅ Has detenido la propagación. Objetivos protegidos: " + objetivosSalvados);
        clearInterval(propagacion);
    } else {
        // 👉 Solo reiniciar si NO terminó el juego
        clearInterval(propagacion);
        propagacion = setInterval(async () => {
            await autoPaso();
            await actualizarEstadisticas();
        }, 20000); // Reinicia el contador
    }

    document.getElementById('nodoBloquear').value = '';
}


// Función para marcar un nodo como protegido
function proteccionNodo(id) {
    // Actualiza el color del nodo o el estado visual para indicar protección
    network.body.data.nodes.update({
        id: id,
        color: '#0000cc',  // Color azul para nodos protegidos
        label: '🔒 ' + id  // Agregar ícono de candado al label
    });
}


// Cambiar la función paso para solo ejecutar lo necesario
async function paso() {
    const nodo = document.getElementById('nodoBloquear').value.toUpperCase();

    if (nodo) {
        proteccionNodo(nodo);  // 🔒 Aplicar protección visual inmediata
    }

    await actualizarColores();
    await actualizarEstadisticas();
}


window.onload = () => {
    cargarGrafo();
    mostrarCentralidades();
    propagacion = setInterval(async () => {
        await autoPaso();
        await actualizarEstadisticas();
    }, 20000); // Cada 20 segundos
};

