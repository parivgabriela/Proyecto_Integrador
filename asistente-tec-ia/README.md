# Asistente Tec-IA

**Asistente Tec-IA** es una aplicación de asistente virtual desarrollada como trabajo integrador de la carrera de **Tecnicatura Superior en Ciencia de Datos e IA** del **IFTS 24**. Esta herramienta está diseñada para apoyar a los estudiantes en su proceso de aprendizaje mediante múltiples funcionalidades basadas en inteligencia artificial.
El sistema utiliza el sistema RAG

## Material para las personas curiosas

### 🤖 Chatbot Inteligente
- El asistente tec-IA utiliza llama 3.2 como modelo LLM (en caso de querer modificarlo se debe repetir el proceso de descargar el archivo existente en ollama). Primero se procesan los archivos que se encuentran es app/static/pdfs.


### 📄 Resumidor de Textos
- Capacidad para resumir archivos de texto de hasta **1200 palabras** esto también se puede modificar
- Utiliza el modelo **llama3.2:latest** de meta. Se puede modificar por otro, pero debe estar descargado desde ollama
- Genera resúmenes concisos y coherentes

### 🔍 Extractor de Palabras Clave
- Implementado con **KeyBERT**
```python
Esta funcionalidad puede devolver de una a dos palabras
[
  ('palabras clave', 0.78),
  ('texto', 0.75),
  ('extracción', 0.72),
  ('ejemplo de', 0.65),
  ('probar', 0.62)
]
```

### ❓ Módulo de Preguntas Frecuentes (FAQ)
- Este sistema fue creado en base a ahorra tiempo a la hora de responder dudas comunes entre los estudiantes. El archivo es totalmente customizable. ver la estructura y copiar el formato en data/faq.json

### Archivos Temporales vs Permanentes
- La aplicación maneja dos tipos de almacenamientos para los archivos a ser procesados. EL chatbot Tec-IA trabaja con archivos permanentes. Y procesamiento también lo es. Por eso una vez que se entrene el modelo no es necesario volver a presionar el botón nuevamente.
- Chatear con PDF: este módulo utiliza la carpeta temporal *uploads*, que se puede encontrar si se ejecuta ```tempfile.gettempdir()```. Antes de iniciar se verifica que la carpeta exista y de no ser así poder crearla y en caso de que exista limpiar todo el contenido. La base de conocimiento también es temporal, lo que se haya procesado previamente ya fue eliminado.

### Crear Entorno Virtual con Conda

Este paso es necesario para evitar que las versiones previamente instaladas no interfieran con las librerias que requiere el asiste y viceversa.

```bash
conda create --name asistente-tec-ia python=3.10
conda activate asistente-tec-ia
```


### Ejecución Manual
Si prefieres ejecutar manualmente:
```bash
conda activate asistente-tec-ia
python3 run.py
```

## Estructura del Proyecto

```
asistente-tec-ia/
├── app/                  # Aplicación principal
    ├── static/           # Archivos estáticos (CSS, JS, imágenes)
    ├── templates/        # Archivos html
├── data/                 # Archivos Json con FAQ
├── logs/                 # archivo temporal es diferente en cada usuario
├── vectordb/             # Base de datos donde se almacena los archivos procesados
├── .gitignore            # Lista de archivos que no son subidos al repositorio
├── requirements.txt       # Dependencias de Python
├── start.bat             # Script de inicio para Windows
├── start.sh              # Script de inicio para Linux
├── static/pdf               
└── README.md            # Este archivo
```

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

Gabriela Pari Vaca

Para consultas académicas o técnicas, contactar a databypari@gmail.com
