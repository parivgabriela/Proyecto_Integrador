// Función para mostrar el progreso en la interfaz
function updateProgressBar(progress) {
    // Si tienes una barra de progreso en tu UI:
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.style.width = progress + '%';
        progressBar.textContent = progress + '%';
    }
    
    // Alternativa: mensaje en la pantalla de carga
    const loadingText = document.getElementById('loadingText');
    if (loadingText) {
        loadingText.textContent = `Procesando archivos: ${progress}%`;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const uploadBtn = document.getElementById('uploadBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const uploadSection = document.getElementById('uploadSection');
    const downloadSection = document.getElementById('downloadSection');
    const fileUpload = document.getElementById('fileUpload');
    const dropZone = document.getElementById('dropZone');
    const fileList = document.getElementById('fileList');
    const urlInput = document.getElementById('urlInput');
    const processUploadBtn = document.getElementById('processUploadBtn');
    const processDownloadBtn = document.getElementById('processDownloadBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const chatWrapper = document.getElementById('chatWrapper');
    
    let uploadedFiles = [];
    const socket = io();
    
    // Mostrar sección de carga de archivos por defecto
    uploadSection.classList.add('active');
    
    // Event listeners para cambiar entre secciones
    uploadBtn.addEventListener('click', function() {
        uploadSection.classList.add('active');
        downloadSection.classList.remove('active');
    });
    
    downloadBtn.addEventListener('click', function() {
        downloadSection.classList.add('active');
        uploadSection.classList.remove('active');
    });
            
    // Event listeners para el drag and drop
    dropZone.addEventListener('click', function() {
        fileUpload.click();
    });
    
    fileUpload.addEventListener('change', handleFileSelect);
    
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.style.borderColor = '#4a86e8';
    });
    
    dropZone.addEventListener('dragleave', function() {
        dropZone.style.borderColor = '#ccc';
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.style.borderColor = '#ccc';
        
        if (e.dataTransfer.files.length > 0) {
            handleFiles(e.dataTransfer.files);
        }
    });
            
    // URL input validation
    urlInput.addEventListener('input', function() {
        processDownloadBtn.disabled = !urlInput.value.trim();
    });
    
    // Process buttons event listeners
    processUploadBtn.addEventListener('click', function() {
        if (uploadedFiles.length > 0) {
            processFiles('/subir_archivos_procesar');
        }
    });
    
    processDownloadBtn.addEventListener('click', function() {
        const url = urlInput.value.trim();
        if (url) {
            processUrlDownload('/descargar_archivo_url', url);
        }
    });
    
    // Functions
    function handleFileSelect(e) {
        handleFiles(this.files);
    }
            
    function handleFiles(files) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (file.type === 'application/pdf' || file.type ==='text/plain') {
                uploadedFiles.push(file);
                
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <i class="fas fa-file-pdf"></i>
                    <span>${file.name} (${formatFileSize(file.size)})</span>
                `;
                fileList.appendChild(fileItem);
            }
        }
        
        processUploadBtn.disabled = uploadedFiles.length === 0;
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function processFiles(endpoint) {
        showLoading();
        
        const formData = new FormData();
        uploadedFiles.forEach(file => {
            formData.append('files', file);
        });

        fetch(endpoint, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                // Si la respuesta no es OK, lanza un error con el mensaje del backend
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }).catch(() => {
                    // Si no se puede parsear JSON, lanzar un error genérico
                    throw new Error(`HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            showChat();
            console.log("Respuesta completa del backend:", data);
        })
        .catch(error => {
            hideLoading();
            alert('Error al procesar los archivos: ' + error);
        });
    }
            
    function processUrlDownload(endpoint, url) {
        showLoading();

        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            showChat();
        })
        .catch(error => {
            hideLoading();
            alert('Error al descargar el archivo: ' + error);
        });
    }
  
    function showLoading() {
        loadingOverlay.classList.add('active');
    }

    function hideLoading() {
        loadingOverlay.classList.remove('active');
    }

    function showChat() {
        document.querySelector('.file-manager').style.display = 'none';
        chatWrapper.classList.add('active');
    }
});