# Asistente Tec-IA

### Proyecto Integrador,&nbsp;&nbsp;Tecnicatura Superior ciencia de datos e IA, &nbsp;&nbsp;IFTS24

**Profesor:** Erick Ravelo&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; **Alumna:** Gabriela Pari Vaca

---------
## Descripción del Proyecto

**Asistente Tec-IA** es una aplicación de asistente virtual desarrollada como trabajo integrador de la carrera de **Tecnicatura Superior en Ciencia de Datos e IA** del **IFTS 24**. Esta herramienta está diseñada para apoyar a los estudiantes en su proceso de aprendizaje mediante múltiples funcionalidades basadas en inteligencia artificial.

## Características Principales

### 🤖 Chatbot Inteligente
- Asistente virtual alimentado por una base de datos custom cargada con información específica de la carrera y las materias
- Responde consultas relacionadas con el contenido académico
- Interfaz conversacional intuitiva

### 📄 Resumidor de Textos
- Capacidad para resumir archivos de texto de hasta **1200 palabras**
- Utiliza el modelo de **ollama-llama3.2** de Meta (`llama3.2:latest`)
- Genera resúmenes concisos y coherentes

### 🔍 Extractor de Palabras Clave
- Identificación automática de palabras clave en textos
- Implementado con **KeyBERT**
- Ayuda a identificar los conceptos más relevantes de un documento

### ❓ Módulo de Preguntas Frecuentes (FAQ)
- Sistema de preguntas frecuentes para acelerar las respuestas
- Búsqueda inteligente en base a las consultas del usuario
- Crea una base de conocimiento interactiva para que los estudiantes pongan a prueba sus conocimientos

## Requisitos del Sistema

### Software Necesario
- **Python 3.10+** (desarrollado en Python 3.10)
- **Ollama** con el modelo **Llama 3.2**
- **Git** para clonar el repositorio
- **Conda** (recomendado para gestión de entornos)

### Sistemas Operativos Compatibles
- Windows 10/11
- Linux (Ubuntu, Debian, CentOS, etc.)

## Instalación

### 1. Clonar el Repositorio
```bash
git clone git@github.com:parivgabriela/Proyecto_Integrador.git
cd asistente-tec-ia
```

### 2. Instalar Ollama y el Modelo Llama 3.2

#### Para Windows:
1. Descargar Ollama desde: https://ollama.com/download
2. Instalar el ejecutable
3. Abrir terminal y ejecutar:
```bash
ollama run llama3.2
```

#### Para Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.2
```

### 3. Crear Entorno Virtual con Conda
Puede ser otro entorno

```bash
conda create --name asistente-tec-ia python=3.10
conda activate asistente-tec-ia
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Ejecución de la Aplicación

### Windows
Ejecutar el archivo por lotes incluido:
```bash
start.bat
```

### Linux
Ejecutar el script shell:
```bash
chmod +x start.sh
./start.sh
```
### Al fin! Ir al navegador
Una vez ejecutada la aplicación, ir al link que aparece en la terminal o pegar el siguiente link
 http://127.0.0.1:5000

### Antes de usar el asistente Tec-IA por primera vez
Antes de utilizar el chat de asistente Tec-IA hace clic en "Entrenar modelo"

### Ejecución Manual
Si prefieres ejecutar manualmente:
```bash
conda activate asistente-tec-ia
python3 run.py
```

## Estructura del Proyecto

```
Proyecto_Integrador      
├── asistente-tec-ia/
    ├── app/                  # Aplicación principal
    ├── start.bat             # Script de inicio para Windows
    ├── start.sh              # Script de inicio para Linux
    ...          
└── README.md                 # Archivo Readme
```

## Uso de la Aplicación

### Chatbot Tec-IA
1. Inicia la aplicación
2. Escribe tu consulta en el chat
3. El asistente responderá basándose en la base de datos de la carrera

### Chatear con PDF personalizado
1. Selecciona del menú "Chatear con PDF"
2. Carga tu archivo PDF o TXT y luego hace clic en "Procesar archivos"
3. El asistente responderá basándose en la información cargada.

### Chatear con Llama
1. Selecciona del menú "Chatear con Llama3.2"
2. Escribe tu consulta. El modelo esta especializado para responderte como un experto en ciencia de datos e IA, junto con programación en python

### Resumidor de Textos
1. Selecciona del menú "Analizar texto"
2. Carga tu archivo de texto o pega el texto (máximo 1200 palabras).
3. Selecciona la opción "Resumir Texto"

### Extractor de Palabras Clave
1. Selecciona del menú "Analizar texto"
2. Carga tu archivo de texto o pega el texto (máximo 1200 palabras).
3. Selecciona la opción "Extraer Palabras Claves"

### Preguntas Frecuentes
1. Navega al módulo de FAQ
2. Explora las preguntas frecuentes disponibles
3. Pon a prueba tu conocimiento respondiendo las preguntas

## Solución de Problemas

### Error: "Ollama not found"
- Verifica que Ollama esté instalado y en el PATH del sistema
- Asegúrate de que el modelo Llama 3.2 esté descargado

### Error: "Module not found"
- Verifica que el entorno virtual esté activado
- Reinstala las dependencias: `pip install -r requirements.txt`

### Problemas con CUDA (Linux)
- Si tienes GPU NVIDIA, instala los drivers apropiados
- Para CPU únicamente, las dependencias funcionarán sin configuración adicional

## Contribución

Este proyecto fue desarrollado como trabajo integrador académico. Para contribuciones:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autores

- **Gabriela Juliana Pari Vaca**
- **IFTS 24**

## Contacto

databypari@gmail.com

---

*Desarrollado con ❤️ y mucha paciencia*

