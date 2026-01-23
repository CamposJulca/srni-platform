document.addEventListener("DOMContentLoaded", function () {

    const zipInput = document.getElementById("zipFile");
    const firmaInput = document.getElementById("firmaFile");

    const uploadBtn = document.getElementById("uploadZipBtn");
    const signBtn = document.getElementById("signBtn");
    const pdfBtn = document.getElementById("pdfBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const clearLogsBtn = document.getElementById("clearLogsBtn");

    const posicionarFirmaBtn =
        document.getElementById("posicionarFirmaBtn");

    const uploadStatus = document.getElementById("status-upload");
    const signStatus = document.getElementById("signStatus");
    const pdfStatus = document.getElementById("pdfStatus");
    const downloadStatus = document.getElementById("downloadStatus");

    const logConsole = document.getElementById("logConsole");

    /* =========================
       Logs
       ========================= */
    function pushLog(message, type = "info") {
        const line = document.createElement("div");
        line.className = `log ${type}`;
        const time = new Date().toLocaleTimeString();
        line.textContent = `[${time}] ${message}`;
        logConsole.appendChild(line);
        logConsole.scrollTop = logConsole.scrollHeight;
    }

    clearLogsBtn.addEventListener("click", function () {
        logConsole.innerHTML = "";
        pushLog("Logs limpiados por el usuario", "info");
    });

    function setStatus(el, msg, color) {
        el.textContent = msg;
        el.style.color = color;
    }

    /* =========================
       Paso 1: Cargar ZIP + Firma
       ========================= */
    uploadBtn.addEventListener("click", async function () {

        if (!zipInput.files.length || !firmaInput.files.length) {
            setStatus(uploadStatus, "Seleccione ZIP y firma PNG", "red");
            pushLog("Error: ZIP o firma no seleccionados", "error");
            return;
        }

        const formData = new FormData();
        formData.append("zip_file", zipInput.files[0]);
        formData.append("firma_file", firmaInput.files[0]);

        setStatus(uploadStatus, "Cargando archivos…", "black");
        pushLog("Cargando ZIP y firma…", "info");

        try {
            const r = await fetch("/automatizacion/cargar-zip/", {
                method: "POST",
                body: formData
            });

            if (!r.ok) {
                const text = await r.text();
                throw new Error(text);
            }

            const d = await r.json();

            setStatus(
                uploadStatus,
                `ZIP cargado (${d.total_archivos})`,
                "green"
            );

            pushLog(
                `ZIP procesado (${d.total_archivos} documentos)`,
                "ok"
            );

            signBtn.disabled = false;

        } catch (e) {
            setStatus(uploadStatus, e.message, "red");
            pushLog(e.message, "error");
        }
    });

    /* =========================
       Paso 2: Preparar documentos
       ========================= */
    signBtn.addEventListener("click", function () {

        setStatus(signStatus, "Documentos preparados", "green");
        pushLog("Documentos listos para posicionar firma", "ok");

        posicionarFirmaBtn.disabled = false;
    });

    /* =========================
       Paso 2.5: Posicionar firma
       ========================= */
    posicionarFirmaBtn.addEventListener("click", function () {

        pushLog(
            "Abriendo pantalla de posicionamiento de firma",
            "info"
        );

        window.open(
            "/automatizacion/posicionar-firma/",
            "_blank"
        );
    });

    /* =========================
       MENSAJE DESDE POSICIONAR FIRMA
       ========================= */
    window.addEventListener("message", function (event) {

        if (!event.data || event.data.tipo !== "firma_guardada") {
            return;
        }

        pushLog("Posición de firma confirmada", "ok");
        setStatus(signStatus, "Firma posicionada", "green");

        pdfBtn.disabled = false;
    });

    /* =========================
       Paso 3: Generar y firmar PDFs
       ========================= */
    pdfBtn.addEventListener("click", async function () {

        setStatus(pdfStatus, "Generando PDFs…", "black");
        pushLog("Generando y firmando PDFs…", "info");

        try {
            const r = await fetch("/automatizacion/generar-pdfs/", {
                method: "POST"
            });

            if (!r.ok) {
                const text = await r.text();
                throw new Error(text);
            }

            const d = await r.json();

            setStatus(
                pdfStatus,
                `PDFs generados (${d.total_pdfs})`,
                "green"
            );

            pushLog(
                `PDFs generados y firmados: ${d.total_pdfs}`,
                "ok"
            );

            downloadBtn.disabled = false;

        } catch (e) {
            setStatus(pdfStatus, e.message, "red");
            pushLog(e.message, "error");
        }
    });

    /* =========================
       Paso 4: Descargar ZIP final
       ========================= */
    downloadBtn.addEventListener("click", function () {

        setStatus(downloadStatus, "Descargando ZIP…", "black");
        pushLog("Descargando ZIP final…", "info");

        window.location.href =
            "/automatizacion/descargar-zip/";

        setStatus(downloadStatus, "ZIP descargado", "green");
        pushLog("Proceso finalizado correctamente", "ok");
    });
});
