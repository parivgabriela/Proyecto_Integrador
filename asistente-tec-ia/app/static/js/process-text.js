document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias a Elementos ---
    const body = document.body;
    const textInput = document.getElementById('text-input');
 
    const initialView = document.getElementById('initial-view');
    const editorView = document.getElementById('editor-view');
    const loadingView = document.getElementById('loading-view');
    const resultsView = document.getElementById('results-view');

    const pasteTextBtn = document.getElementById('pegar-texto-btn');
    const fileUploadInputBtn = document.getElementById('subir-archivo-btn');
    const fileInput = document.getElementById('file-input');

    const wordCountDisplay = document.getElementById('word-count-display');
    const actionButtons = document.getElementById('action-buttons');
    const backToInitialBtn = document.getElementById('back-to-initial-btn');
    const clearTextBtn = document.getElementById('clear-text-btn'); // Nuevo

    const summarizeBtn = document.getElementById('summarize-btn');
    const keywordsBtn = document.getElementById('keywords-btn');

    const resultsTitle = document.getElementById('results-title');
    const resultsContent = document.getElementById('results-content');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');

    const MAX_WORDS = 2000; // Límite de palabras

    // --- Funciones de Navegación entre Vistas ---
    function showView(viewToShow) {
        [initialView, editorView, loadingView, resultsView].forEach(view => {
            view.classList.add('hidden');
        });
        viewToShow.classList.remove('hidden');
    }

    function openEditor() {
        showView(editorView);
        textInput.focus();
        toggleActionButtons();
        updateWordCount(); // Actualizar contador al abrir el editor
    }

    // --- Manejadores de Eventos ---
    pasteTextBtn.addEventListener('click', openEditor);
        
    backToInitialBtn.addEventListener('click', () => {
         textInput.value = '';
         updateWordCount(); // Resetear contador
         showView(initialView);
    });

    fileUploadInputBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file && file.type === 'text/plain') {
            const reader = new FileReader();
            reader.onload = (e) => {
                textInput.value = e.target.result;
                openEditor();
            };
            reader.readAsText(file);
        }
        fileInput.value = ''; // Reset para poder subir el mismo archivo de nuevo
    });

        textInput.addEventListener('input', () => {
            toggleActionButtons();
            updateWordCount();
        });
        
        function toggleActionButtons() {
            if(textInput.value.trim().length > 0) {
                actionButtons.classList.remove('hidden');
            } else {
                actionButtons.classList.add('hidden');
            }
        }

        // --- Lógica del Contador de Palabras ---
        function updateWordCount() {
            const text = textInput.value.trim();
            const words = text === '' ? 0 : text.split(/\s+/).length;
            wordCountDisplay.textContent = `Palabras: ${words} / ${MAX_WORDS}`;
            if (words > MAX_WORDS) {
                wordCountDisplay.classList.add('text-red-500');
                wordCountDisplay.classList.remove('text-gray-500', 'dark:text-gray-400');
            } else {
                wordCountDisplay.classList.remove('text-red-500');
                wordCountDisplay.classList.add('text-gray-500', 'dark:text-gray-400');
            }
        }

        // --- Botón Limpiar ---
        clearTextBtn.addEventListener('click', () => {
            textInput.value = '';
            toggleActionButtons();
            updateWordCount();
            textInput.focus();
        });

        summarizeBtn.addEventListener('click', () => processTextAndFile('summarize')); //processRequest
        keywordsBtn.addEventListener('click', () => processTextAndFile('extract_keywords'));

        newAnalysisBtn.addEventListener('click', () => {
            textInput.value = '';
            updateWordCount(); // Resetear contador
            showView(initialView);
        });

        // --- Lógica de Procesamiento ---
        const processTextAndFile = async (actionType) => {
            const text = textInput.value.trim();
            const file = fileInput.files[0];

            if (!text && !file) { // Se podría requerir al menos uno de los dos.
                alert("El texto no puede estar vacío.");
                return;
            }
        
            const words = text ? text.split(/\s+/).length : 0;
            if (words > MAX_WORDS) {
                alert(`El texto excede el límite de ${MAX_WORDS} palabras. Por favor, reduce la cantidad de texto.`);
                return;
            }
        
            showView(loadingView);
        
            try {
                const formData = new FormData();
                formData.append('action', actionType);
                formData.append('textInput', text);
                if (file) {
                    formData.append('uploadedFile', file);
                }
            
                const response = await fetch('/procesar_texto_y_archivo', {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) {
                    let errorMessage = "Ocurrió un error en el servidor.";
                    const contentType = response.headers.get('Content-Type');

                    if (contentType && contentType.includes("application/json")) {
                        const errorResult = await response.json();
                        errorMessage = errorResult.error || JSON.stringify(errorResult);
                    } else {
                        errorMessage = await response.text();
                    }

                    throw new Error(`Error ${response.status}: ${errorMessage}`);
                }

                const result = await response.json();

                resultsTitle.textContent = result.title || `Resultados de ${actionType === 'summarize' ? 'Resumen' : 'Extracción de Palabras Clave'}`;

                if (result.error) {
                    resultsContent.innerHTML = `<div class="error-message">${result.error}</div>`;
                } else {
                    if (actionType === 'summarize') {
                        resultsContent.innerHTML = `<p>${result.summary || 'No se pudo generar el resumen.'}</p>`;
                    } else if (actionType === 'extract_keywords') {
                        if (result.keywords && Array.isArray(result.keywords) && result.keywords.length > 0) {
                            resultsContent.innerHTML = `<ul>${result.keywords.map(kw => `<li>${kw}</li>`).join('')}</ul>`;
                        } else {
                            resultsContent.innerHTML = '<p>No se encontraron palabras clave.</p>';
                        }
                    } else {
                        resultsContent.innerHTML = '<p>Formato de resultado desconocido.</p>';
                    }
                }
            
            } catch (error) {
                resultsTitle.textContent = "Error en la Solicitud";
                resultsContent.innerHTML = `<div class="error-message">${error.message}</div>`;
            } finally {
                showView(resultsView);
            }
        };
});