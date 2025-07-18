import chromadb
import re
import logging
import unicodedata
from app.config.files_config import load_json_file, save_json_file, update_faq_frequency, FAQ_FILE, FAQ_USER_FILE
from .questions import get_anwser
from .constants_process import MODEL_CUSTOM_PDF, MODEL_LLAMA

chroma_client = chromadb.PersistentClient(path="chroma_cache")
collection = chroma_client.get_or_create_collection(name="cache_respuestas")


def list_metadatas(collection):
    # Recuperar todos los documentos y sus metadatos
    stored_data = collection.get()
    metadatas = stored_data["metadatas"]  # Acceder a los metadatos
    unique_metadatas = set()
    # Imprimir cada conjunto de metadatos
    for metadata in metadatas:
        if metadata:
            unique_metadatas.add(str(metadata["file_name"]))
    if len(unique_metadatas) > 0:
        print(f"Listar archivos cargados:\n{unique_metadatas}")


def process_question_nlp(question: str) -> str:
    """Normaliza una pregunta para usarla como clave."""
    texto = question.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z0-9\s]', '', texto) # elimina los signos de puntuación
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def get_next_user_faq_id():
    """Genera el próximo ID para una pregunta de usuario."""
    user_faq_data = load_json_file(FAQ_USER_FILE)
    if not user_faq_data:
        return 1000 # El primer ID para FAQs de usuario
    return max(item["id"] for item in user_faq_data) + 1


def correct_text_format(pregunta: str) -> str:
    """
    Normaliza una cadena de texto para formatearla como una pregunta en español.
    - Agrega tildes a las palabras interrogativas comunes (qué, cómo, cuándo, etc.).
    - Añade los signos de interrogación al principio y al final si la frase
      parece ser una pregunta.
    - Pone en mayúscula la primera letra.

    Args:
        pregunta (str): La pregunta del usuario sin formato.

    Returns:
        str: La pregunta formateada correctamente.
    """
    pregunta_limpia = pregunta.strip().lower()

    palabras_interrogativas = {
        "que": "qué",
        "cual": "cuál",
        "cuales": "cuáles",
        "quien": "quién",
        "quienes": "quiénes",
        "como": "cómo",
        "cuando": "cuándo",
        "cuanto": "cuánto",
        "cuanta": "cuánta",
        "cuantos": "cuántos",
        "cuantas": "cuántas",
        "donde": "dónde",
        "adonde": "adónde",
        "por que": "por qué"
    }

    for sin_tilde, con_tilde in palabras_interrogativas.items():
        pregunta_limpia = re.sub(r'\b' + sin_tilde + r'\b', con_tilde, pregunta_limpia)

    primera_palabra = pregunta_limpia.split()[0]
    if primera_palabra in palabras_interrogativas.values():
        if not pregunta_limpia.startswith('¿'):
            pregunta_limpia = '¿' + pregunta_limpia
        if not pregunta_limpia.endswith('?'):
            pregunta_limpia += '?'

    if len(pregunta_limpia) > 1:
        if pregunta_limpia.startswith('¿'):
            pregunta_final = pregunta_limpia[0] + pregunta_limpia[1].upper() + pregunta_limpia[2:]
        else:
            pregunta_final = pregunta_limpia[0].upper() + pregunta_limpia[1:]
    else:
        pregunta_final = pregunta_limpia

    return pregunta_final


def process_user_query(query: str, model_type: str):
    """
    Procesa la pregunta del usuario: busca en las FAQs existentes,
    si no la encuentra, genera una nueva respuesta y la almacena.
    """
    response = None
    user_question_lower = process_question_nlp(query)
    if model_type == MODEL_LLAMA:
        response = get_anwser(query, model_type)
        return response
    # 1. Cargar todas las FAQs (predefinidas y de usuario)
    faq_data = load_json_file(FAQ_FILE)
    faq_user_data = load_json_file(FAQ_USER_FILE)
    
    all_faqs = faq_data + faq_user_data
    
    found_faq = None
    for faq in all_faqs:
        if user_question_lower == process_question_nlp(faq["pregunta"]):
            found_faq = faq
            break
    
    if found_faq:
        # La pregunta existe, brindamos la respuesta y sumamos el contador
        logging.info(f"Pregunta encontrada en FAQ\nRespuesta (ID {found_faq['id']}): {found_faq['respuesta']}")
        update_faq_frequency(found_faq["id"])
        response = found_faq['respuesta']
    else:
        # La pregunta no existe, llamamos a answer_question, almacenamos y sumamos el contador
        response = get_anwser(query, model_type)

        # don't save
        if not model_type == MODEL_CUSTOM_PDF and "No encontré información" not in response:
            new_faq_id = get_next_user_faq_id()
            query_with_format = correct_text_format(query)
            new_faq_entry = {
                "id": new_faq_id,
                "pregunta": query_with_format,
                "respuesta": response
            }
        
            faq_user_data.append(new_faq_entry)
            save_json_file(faq_user_data, FAQ_USER_FILE)
        
            update_faq_frequency(new_faq_id) # Inicializa el contador para la nueva FAQ
            logging.info(f"Nueva pregunta almacenada (ID {new_faq_id}): {query_with_format}")

    return response
