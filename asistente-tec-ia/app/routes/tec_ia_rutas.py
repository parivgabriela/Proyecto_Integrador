import os
import logging
import requests
from urllib.parse import urlparse
from app.extensions import socketio
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.config.files_config import load_json_file, FAQ_FILE, FAQ_FREQ_FILE
from app.services.question_process import process_user_query
from app.services.files_pdf_process import list_pdf_files, process_pdf_files_save_collection, UPLOAD_USER_PATH, KNOWLEDGE_BASE_PATH
from app.services.get_keywords_text import extract_keywords
from app.services.summarize_text import resumir_texto_ai
from app.services.constants_process import MODEL_TEC_IA, MODEL_CUSTOM_PDF, MODEL_LLAMA

tec_ia_bot = Blueprint("tec_ia_bot", __name__)


@tec_ia_bot.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@tec_ia_bot.route('/pdfs/<filename>')
def mostrar_pdf(filename):
    return render_template('view_pdf.html', filename=filename)


@tec_ia_bot.route('/listar_archivos')
def listar_pdf():
    lista_pdfs = list_pdf_files(KNOWLEDGE_BASE_PATH)
            # "id": 2, revisar
            # "nombre": "Documento 2", 
            # "descripcion": "Descripción del documento 2"
  
    return render_template('menu_pdfs.html', documentos=lista_pdfs)

@tec_ia_bot.route('/entrenar_modelo')
def entrenar_modelo():
    process_pdf_files_save_collection(KNOWLEDGE_BASE_PATH, MODEL_TEC_IA)

    return render_template('index.html', respuesta="Modelo entrenado ok")


@tec_ia_bot.route("/chatear_archivo", methods=["GET"])
def chatear_archivos_usuario():
    return render_template("chatear_pdf.html")

@tec_ia_bot.route("/info_tec_ia", methods=["GET"])
def mostrar_info_tec_ia():
    return render_template("info_tec_ia.html")


@socketio.on("chat_personalizado")
def chat_personalizado(query):
    logging.info(f"Mensaje recibido por el modelo {MODEL_CUSTOM_PDF}")
    respuesta = process_user_query(query=query, model_type=MODEL_CUSTOM_PDF)

    socketio.send(respuesta)


@socketio.on("chat_tec_ia")
def handle_message(msg):
    logging.info(f"Mensaje recibido tec_ia")
    respuesta = process_user_query(query=msg, model_type=MODEL_TEC_IA)

    socketio.send(respuesta)

@socketio.on("chat_with_llama")
def chat_with_llama(query):
    logging.info(f"Mensaje recibido llama")
    respuesta = process_user_query(query=query, model_type=MODEL_LLAMA)

    socketio.send(respuesta)

@tec_ia_bot.route("/chatear_modelo_llama", methods=["GET"])
def chatear_modelo_llama():
    return render_template("chatear_modelo_llama.html")

@socketio.on("procesando_archivos")
def procesando_archivos():
    logging.info("Procesando archivos")
    socketio.send("Iniciando proceso de guardar la información a la colección")
    process_pdf_files_save_collection(UPLOAD_USER_PATH, MODEL_CUSTOM_PDF)


@socketio.on("proceso_archivos_completado")
def procesando_archivos_completado():
    socketio.send("Se finalizo proceso de guardar la información a la colección")


@tec_ia_bot.route('/subir_archivos_procesar', methods=['POST'])
def subir_archivo():
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No se encontraron archivos en la petición"}), 400
    except Exception as e:
        logging.error(f"Error al subir archivos: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

    uploaded_files_info = []
    errors = []

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400

        if file:
            try:
                filename = secure_filename(file.filename)
                # Accede a UPLOAD_FOLDER desde la configuración de la aplicación
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files_info.append({
                    "filename": filename,
                    "ruta": file_path,
                    "status": "success"
                })
            except Exception as e:
                errors.append({"filename": file.filename, "error": f"Error al guardar: {str(e)}"})
        
    if uploaded_files_info:
        message = "Archivos procesados exitosamente."
        procesando_archivos()
        if errors:
            message += " Algunos archivos tuvieron errores."
        return jsonify({
            "mensaje": message,
            "subidos": uploaded_files_info,
            "errores": errors
        }), 200
    else:
        return jsonify({
            "error": "No se pudo subir ningún archivo.",
            "errores": errors
        }), 400    

@tec_ia_bot.route('/descargar_archivo_url', methods=['POST'])
def descargar_archivo_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    try:
        # Descargar contenido desde la URL
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Obtener nombre del archivo desde la URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = 'archivo_descargado'

        file_path = os.path.join(UPLOAD_USER_PATH, filename)

        # Guardar archivo localmente
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return jsonify({
            'message': 'Archivo descargado correctamente',
            'filename': filename,
            'filepath': file_path
        })

    except requests.RequestException as e:
        return jsonify({'error': f'Error al descargar el archivo: {str(e)}'}), 500


@tec_ia_bot.route("/analizar_texto", methods=["GET"])
def analizar_archivo():
    return render_template("analizar_texto.html")

@tec_ia_bot.route('/procesar_texto_y_archivo', methods=['POST'])
def procesar_texto_y_archivo():
    try:
        # Get text from request
        text_content = request.form.get('textInput', '')
        uploaded_file = request.files.get('fileUpload')

        file_content = None

        if uploaded_file and uploaded_file.filename != '':
            # Read the file content
            file_content = uploaded_file.read().decode('utf-8')
            logging.info(f"File '{uploaded_file.filename}' content: {file_content[:100]}...")

        # summarize or keywords
        action = request.form.get('action')
    
        logging.info(f"Action requested: {action}")

        respuesta = {}
        estado_http = 200
        # Now you can use text_content or file_content based on the action
        if action == "summarize":
            resultado = resumir_texto_ai(text_content)
            respuesta = {
                "title": "Resumen",
                "summary": resultado
            }
        elif action == "extract_keywords":
            resultado = extract_keywords(text_content)
            respuesta = {
                "title": "Palabras Claves",
                "keywords": resultado
            }
        else:
            respuesta = {
                "error": "No se puedo realizar la acción de resumir"
            }
            estado_http = 400
            logging.warning(f"Acción no válida: {action}")
            return jsonify(respuesta), estado_http

        logging.info(f"Acción '{action}' completada exitosamente.")
        return jsonify(respuesta), estado_http

    except Exception as e:
        logging.error(f"Error procesando la solicitud: {str(e)}")
        return jsonify({
            "detalle": str(e),
            "error": "Se produjo un error al procesar la solicitud."
        }), 500

@tec_ia_bot.route('/get_view_faq', methods=['GET'])
def get_view_faq():
    return render_template("faq.html")

@tec_ia_bot.route('/get_faq', methods=['GET'])
def obtener_faq():
    faq_info = load_json_file(FAQ_FILE)
    print("type",type(faq_info))
    return jsonify(faq_info), 200

@tec_ia_bot.route('/get_faq_ranking', methods=['GET'])
def get_faq_ranking():
    faq_data = load_json_file(FAQ_FILE)               # { "1": "¿Qué es X?", "2": "¿Cómo usar Y?" }
    freq_data = load_json_file(FAQ_FREQ_FILE)         # [ { "id": "1", "frecuencia": 20 }, ... ]

    # Ordenar por frecuencia descendente
    ranked = sorted(freq_data, key=lambda x: x['frecuencia'], reverse=True)
    
    faq_data_dict = {item["id"]: item["pregunta"] for item in faq_data}
    # Combinar preguntas con su frecuencia
    result = []
    for item in ranked:
        q_id = item['id_pregunta']
        print(q_id)
        pregunta = faq_data_dict.get(q_id, "Pregunta no encontrada")
        print(pregunta)
        result.append({
            "id": q_id,
            "pregunta": pregunta,
            "frecuencia": item['frecuencia']
        })

    return jsonify(result), 200

