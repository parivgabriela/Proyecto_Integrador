const toggleThemeButton = document.getElementById('toggleTheme');

// Configuración del tema (claro/oscuro)
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.className = savedTheme + '-mode';
    
    // Actualizar el icono según el tema
    if (savedTheme === 'dark') {
        toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

// Cambiar entre tema claro y oscuro
function toggleTheme() {
    const isDarkMode = document.body.classList.contains('dark-mode');
    
    if (isDarkMode) {
        document.body.className = 'light-mode';
        toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('theme', 'light');
    } else {
        document.body.className = 'dark-mode';
        toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('theme', 'dark');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Cargar tema guardado
    loadTheme();
    
    // Eventos para botones y inputs
    if (toggleThemeButton) {
        toggleThemeButton.addEventListener('click', toggleTheme);
    }
    

});