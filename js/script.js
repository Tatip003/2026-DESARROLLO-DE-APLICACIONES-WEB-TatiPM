const formulario = document.getElementById("formContacto");
const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");

let contador = 0;

const nombreInput = document.getElementById("nombre");
const descripcionInput = document.getElementById("descripcion");
const categoriaInput = document.getElementById("categoria");
const tipoInput = document.getElementById("tipo");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");
const errorTipo = document.getElementById("errorTipo");

const alertaExito = document.getElementById("alertaExito");
const alertaError = document.getElementById("alertaError");


nombreInput.addEventListener("input", validarNombre);
nombreInput.addEventListener("blur", validarNombre);

descripcionInput.addEventListener("input", validarDescripcion);
descripcionInput.addEventListener("blur", validarDescripcion);

categoriaInput.addEventListener("input", validarCategoria);
tipoInput.addEventListener("change", validarTipo);

function validarNombre() {
    if (nombreInput.value.trim().length < 3) {
        errorNombre.textContent = "Mínimo 3 caracteres";
        nombreInput.classList.add("is-invalid");
        nombreInput.classList.remove("is-valid");
        return false;
    }
    errorNombre.textContent = "";
    nombreInput.classList.add("is-valid");
    nombreInput.classList.remove("is-invalid");
    return true;
}

function validarDescripcion() {
    if (descripcionInput.value.trim().length < 10) {
        errorDescripcion.textContent = "Mínimo 10 caracteres";
        descripcionInput.classList.add("is-invalid");
        descripcionInput.classList.remove("is-valid");
        return false;
    }
    errorDescripcion.textContent = "";
    descripcionInput.classList.add("is-valid");
    descripcionInput.classList.remove("is-invalid");
    return true;
}

function validarCategoria() {
    if (categoriaInput.value.trim() === "") {
        errorCategoria.textContent = "Ingrese categoría";
        categoriaInput.classList.add("is-invalid");
        categoriaInput.classList.remove("is-valid");
        return false;
    }
    errorCategoria.textContent = "";
    categoriaInput.classList.add("is-valid");
    categoriaInput.classList.remove("is-invalid");
    return true;
}

function validarTipo() {
    if (tipoInput.value.trim() === "") {
        errorTipo.textContent = "Ingrese tipo";
        tipoInput.classList.add("is-invalid");
        tipoInput.classList.remove("is-valid");
        return false;
    }
    errorTipo.textContent = "";
    tipoInput.classList.add("is-valid");
    tipoInput.classList.remove("is-invalid");
    return true;
}

formulario.addEventListener("submit", function(event) {
    event.preventDefault();

   
    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value.trim();
    const tipo = document.getElementById("tipo").value.trim();

    const valido =
        validarNombre() &&
        validarDescripcion() &&
        validarCategoria() &&
        validarTipo();

    // Validar campos vacíos
    if (!valido) {
         mensaje.textContent = "Corrija los campos antes de registrar.";
    mensaje.className = "text-danger";
    
        alertaError.style.display = "block";
        alertaExito.style.display = "none";
        return;
    }
   
    // Mensaje de éxito
    mensaje.textContent = "Registro agregado correctamente.";
    mensaje.className = "text-success";

    alertaError.style.display = "none";
    alertaExito.style.display = "block";
    
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

    alertaError.style.display = "block";
    alertaExito.style.display = "none";
    formulario.reset();
});