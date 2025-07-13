import json
from os import path
import logging

FOLDER_FAQ = 'data/'
FAQ_FILE = "faq.json"
full_path_faq = FOLDER_FAQ + FAQ_FILE

FAQ_USER_FILE = 'faq_user.json'
FAQ_FREQ_FILE = 'faq_freq.json'

PATH_FAQ_USER = FOLDER_FAQ + FAQ_USER_FILE

def check_json_files():
    if not path.exists(FAQ_USER_FILE):
        save_json_file([], FAQ_USER_FILE)
        # Inicializar faq_freq.json con los IDs de faq.json si no existe o está vacío
    freq_init_data = load_json_file(FAQ_FREQ_FILE)
    if not freq_init_data:
        initial_freq_entries = [{"id_pregunta": faq["id"], "count": 0} for faq in load_json_file(FAQ_FILE)]
        save_json_file(initial_freq_entries, FAQ_FREQ_FILE)


def load_json_file(filename):
    """Carga datos de un archivo JSON. Si no existe, devuelve una lista vacía."""
    if not path.exists(FOLDER_FAQ + filename):
        return []
    try:
        with open(FOLDER_FAQ + filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error(f"No se pudo cargar el archivo {FOLDER_FAQ}")
        return []

def save_json_file(data, filename):
    """Guarda datos en un archivo JSON."""
    with open(FOLDER_FAQ + filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def update_faq_frequency(question_id):
    """Actualiza el contador de frecuencia para una pregunta dada."""
    freq_data = load_json_file(FAQ_FREQ_FILE)
    found = False
    for item in freq_data:
        if item["id_pregunta"] == question_id:
            item["count"] += 1
            found = True
            break
    if not found:
        # Esto debería ocurrir solo si un ID de faq_user.json se añade y no se inicializó en faq_freq.json
        freq_data.append({"id_pregunta": question_id, "count": 1})
    save_json_file(freq_data, FAQ_FREQ_FILE)
