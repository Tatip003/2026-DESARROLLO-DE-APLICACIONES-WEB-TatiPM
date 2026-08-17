
const formulario = document.getElementById("formContacto");
const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");
// Contenedor de los servicios
const listaServicios = document.getElementById("listaServicios");

// Servicios del sistema
const servicios = [
    {
        nombre: "Registro de productos",
        descripcion: "Gestión de productos."
    },
    {
        nombre: "Inventario",
        descripcion: "Control de stock."
    },
    {
        nombre: "Clientes",
        descripcion: "Gestión de clientes."
    }
];

// Arreglo donde se guardarán los registros del formulario
let registros = [];


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
const spinner = document.getElementById("spinnerCarga");

nombreInput.addEventListener("input", validarNombre);
nombreInput.addEventListener("blur", validarNombre);

descripcionInput.addEventListener("input", validarDescripcion);
descripcionInput.addEventListener("blur", validarDescripcion);

categoriaInput.addEventListener("input", validarCategoria);
tipoInput.addEventListener("input", validarTipo);
tipoInput.addEventListener("blur", validarTipo);

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
function mostrarServicios() {

    listaServicios.innerHTML = "";

    servicios.forEach(function(servicio){

        listaServicios.innerHTML += `
            <div class="col-md-4 mb-3">
                <div class="card p-3 shadow h-100">
                    <h5>${servicio.nombre}</h5>
                    <p>${servicio.descripcion}</p>
                </div>
            </div>
        `;

    });

}

function mostrarRegistros(){

    lista.innerHTML="";

    registros.forEach(function(registro,index){

        lista.innerHTML += `

        <div class="card p-3 mt-3">

            <p><strong>Nombre:</strong> ${registro.nombre}</p>

            <p><strong>Descripción:</strong> ${registro.descripcion}</p>

            <p><strong>Categoría:</strong> ${registro.categoria}</p>

            <p><strong>Tipo:</strong> ${registro.tipo}</p>

            <button
                class="btn btn-danger mt-2"
                onclick="eliminarRegistro(${index})">

                Eliminar

            </button>

        </div>

        `;

    });

    total.textContent=registros.length;

}
function eliminarRegistro(indice){

    registros.splice(indice,1);

    mostrarRegistros();

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
    
    // Guardar el registro en el arreglo
// Mostrar spinner
spinner.style.display = "block";

// Simular carga de 2 segundos
setTimeout(function () {

    // Guardar el registro
    registros.push({
        nombre,
        descripcion,
        categoria,
        tipo
    });

    // Actualizar la lista
    mostrarRegistros();

    // Ocultar spinner
    spinner.style.display = "none";

    // Mostrar mensaje de éxito
    alertaError.style.display = "none";
    alertaExito.style.display = "block";

    formulario.reset();

}, 2000);

});
// Mostrar los servicios al iniciar la página
mostrarServicios();