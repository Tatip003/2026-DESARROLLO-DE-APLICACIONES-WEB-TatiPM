const formulario = document.getElementById("formContacto");
const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");

let contador = 0;

formulario.addEventListener("submit", function(event) {

   
    event.preventDefault();

   
    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value.trim();
    const tipo = document.getElementById("tipo").value.trim();

    // Validar campos vacíos
    if (nombre === "" || descripcion === "" || categoria === "" || tipo === "") {
        mensaje.textContent = "Todos los campos son obligatorios.";
        mensaje.className = "text-danger";
        return;
    }

    // Mensaje de éxito
    mensaje.textContent = "Registro agregado correctamente.";
    mensaje.className = "text-success";

    // Crear un nuevo registro
    const registro = document.createElement("div");
    registro.classList.add("card", "p-3", "mt-3");

    registro.innerHTML = `
        <p><strong>nombre:</strong> ${nombre}</p>
        <p><strong>Descripción:</strong> ${descripcion}</p>
        <p><strong>Categoría:</strong> ${categoria}</p>
        <p><strong>Tipo:</strong> ${tipo}</p>
    `;

    // Botón eliminar
    const botonEliminar = document.createElement("button");
    botonEliminar.textContent = "Eliminar";
    botonEliminar.classList.add("btn", "btn-danger", "mt-2");

    botonEliminar.addEventListener("click", function() {
        registro.remove();
        contador--;
        total.textContent = contador;
    });

    registro.appendChild(botonEliminar);
    lista.appendChild(registro);

    contador++;
    total.textContent = contador;

    formulario.reset();
});