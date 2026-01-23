/* =====================================================
   ESTADO GLOBAL
   ===================================================== */

let posicionGuardada = false;
console.log("[JS] posicionGuardada inicial:", posicionGuardada);


/* =====================================================
   PDF.js — CARGA DEL PDF DE PREVISUALIZACIÓN
   ===================================================== */

const pdfUrl = "/media/automatizacion/preview/documento.pdf";
console.log("[JS] PDF URL:", pdfUrl);

const canvas = document.getElementById("pdf-canvas");
const ctx = canvas.getContext("2d");

pdfjsLib.getDocument(pdfUrl).promise.then(pdf => {
    console.log("[JS] PDF cargado correctamente");

    pdf.getPage(1).then(page => {
        console.log("[JS] Página 1 cargada");

        const viewport = page.getViewport({ scale: 1.4 });
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        console.log("[JS] Canvas size:", canvas.width, canvas.height);

        page.render({
            canvasContext: ctx,
            viewport: viewport
        });
    });
});


/* =====================================================
   FIRMA — DRAG & DROP
   ===================================================== */

const firma = document.getElementById("firma");
console.log("[JS] Firma element:", firma);

// Posición y tamaño inicial
firma.style.left = "40px";
firma.style.top = "40px";
firma.style.width = "180px";
firma.style.height = "80px";

let dragging = false;
let offsetX = 0;
let offsetY = 0;

firma.addEventListener("mousedown", e => {
    dragging = true;
    offsetX = e.clientX - firma.offsetLeft;
    offsetY = e.clientY - firma.offsetTop;
    console.log("[JS] Drag start", offsetX, offsetY);
});

document.addEventListener("mousemove", e => {
    if (!dragging) return;
    firma.style.left = `${e.clientX - offsetX}px`;
    firma.style.top = `${e.clientY - offsetY}px`;
});

document.addEventListener("mouseup", () => {
    if (dragging) console.log("[JS] Drag stop");
    dragging = false;
});


/* =====================================================
   GUARDAR POSICIÓN DE LA FIRMA
   ===================================================== */

document.getElementById("guardarBtn").addEventListener("click", () => {

    console.log("[JS] Click Guardar posición");

    const pdfRect = canvas.getBoundingClientRect();
    const firmaRect = firma.getBoundingClientRect();

    const data = {
        page: 1,
        x_ratio: (firmaRect.left - pdfRect.left) / pdfRect.width,
        y_ratio: (pdfRect.bottom - firmaRect.bottom) / pdfRect.height,
        width_ratio: firmaRect.width / pdfRect.width,
        height_ratio: firmaRect.height / pdfRect.height
    };

    console.log("[JS] Data calculada:", data);

    document.getElementById("output").textContent =
        JSON.stringify(data, null, 4);

    fetch("/automatizacion/guardar-posicion-firma/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(resp => {

        if (resp.error) {
            alert("Error guardando la posición");
            return;
        }

        alert("Posición de firma guardada correctamente");
        posicionGuardada = true;

        document.getElementById("continuarBtn").disabled = false;
    })
    .catch(err => {
        console.error("[JS] Error:", err);
        alert("Error guardando posición de firma");
    });
});


/* =====================================================
   CONTINUAR → CERRAR VENTANA Y AVISAR AL PADRE
   ===================================================== */

document.getElementById("continuarBtn").addEventListener("click", () => {

    if (!posicionGuardada) {
        alert("Primero debe guardar la posición de la firma.");
        return;
    }

    if (window.opener && !window.opener.closed) {
        window.opener.postMessage(
            { tipo: "firma_guardada" },
            "*"
        );
    }

    window.close();
});


/* =====================================================
   CANCELAR
   ===================================================== */

document.getElementById("cancelarBtn").addEventListener("click", () => {

    if (confirm("¿Desea cancelar el proceso de firma?")) {
        window.close();
    }
});
