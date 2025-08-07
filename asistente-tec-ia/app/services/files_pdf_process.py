import os
import re
import unicodedata
import logging
import chromadb
import pdfplumber
from werkzeug.utils import secure_filename
from .constants_process import DB_DIRECTORY, sentence_transformer_ef, CHUNK_OVERLAP, CHUNK_SIZE, MODEL_TEC_IA, ALLOWED_EXTENSIONS_chat

# Inicializar ChromaDB
chroma_client = chromadb.PersistentClient(path=DB_DIRECTORY)

collection_tec_ia = chroma_client.get_or_create_collection(
    name="Tec_IA",
    embedding_function=sentence_transformer_ef
)

collection_temp = chromadb.Client().get_or_create_collection(
    name="PDFs_temporal",
    embedding_function=sentence_transformer_ef
)

COLLECTIONS_NAMES = {
    "TEC-IA": collection_tec_ia,
    "CUSTOM-PDF": collection_temp,
    "LLAMA": None
}

def normalize_text(texto: str) -> str:
    """Cleans and normalizes text in Spanish, remove punctuations and spaces like new lines"""
    texto = texto.lower()
    
    # string.punctuation contiene: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    texto = re.sub(r'[^\w\s]', '', texto, flags=re.UNICODE)
    texto = re.sub(r'\s+', ' ', texto).strip()

    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')


def extract_text_from_pdf(full_path):
    """Receive a pdf path then read and return a list with the text"""
    text_by_page = []
    try:
        with pdfplumber.open(full_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_by_page.append(normalize_text(page_text.strip()))
        logging.info(f'Extraccion exitosa de {full_path.split("/")[-1]}')
        return "\n".join(text_by_page)
    except FileNotFoundError:
        logging.error(f"Error: No se encontró el archivo PDF de la ruta {full_path}")
    except Exception as e:
        logging.error(f"Error al procesar el archivo PDF: {e}")
    
    return ""

def extract_text_from_txt(full_path):
    text = None
    with open(full_path, 'r', encoding="utf-8") as f:
        text = f.read()

    return text

def process_pdf_files_save_collection(pdf_path: str, collection_name: str):
    """ Procesa un archivo PDF, crea una base de conocimiento con ChromaDB"""

    files_to_process = list_pdf_files(pdf_path)
    if len(files_to_process) < 1:
        logging.error("Not files in directory not found.")
        return

    collection = COLLECTIONS_NAMES.get(collection_name)
    if not collection:
        logging.error(f"Collection '{collection_name}' not found.")
        return

    total_chunks_processed = 0
    document_text = None
    chunks = []

    for filename in files_to_process:
        full_path = f"{pdf_path}/{filename}"
        extension = filename.split('.')[-1]
        logging.info(f"Extrayendo informacion del archivo {filename}")
        if extension == 'pdf':
            document_text = extract_text_from_pdf(full_path)
        elif extension == 'txt':
            document_text = extract_text_from_txt(full_path)

        if not document_text:
            continue

        # Fusing RecursiveCharacterTextSplitter
        for i in range(0, len(document_text), CHUNK_SIZE - CHUNK_OVERLAP):
            chunk = document_text[i:i + CHUNK_SIZE]
            chunks.append(chunk)

        ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename} for _ in range(len(chunks))]
        
        # .upsert() for idempotency ---
        collection.upsert(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        total_chunks_processed += len(chunks)

    logging.info(f"Se procesaron {len(chunks)} fragmentos del PDF y se agregaron a la base de conocimiento.")


def get_context_from_chroma(query: str, model_type: str):
    context = None
    collection = COLLECTIONS_NAMES.get(model_type)
    if collection:
        result = collection.query(
                query_texts=[query], 
                n_results=3
            )
        context = "\n".join(result['documents'][0]) if result and result['documents'] else "No se encontró información relevante en el documento."

    return context

def save_request_files(path_app_folder, files, endpoint:str):
    
    uploaded_files_info = []
    errors = []
    for file in files:
        if file.filename == '':
            logging.error(f"[{endpoint}] - No se seleccionó ningún archivo")
            errors.append({"error": "No se seleccionó ningún archivo"}), 400

        if file:
            try:
                filename = secure_filename(file.filename)
                # Accede al archivo desde la configuración de la aplicación
                file_path = os.path.join(path_app_folder, filename)
                file.save(file_path)
                uploaded_files_info.append({
                    "filename": filename,
                    "ruta": file_path,
                    "status": "success"
                })
            except Exception as e:
                errors.append({"filename": file.filename, "error": f"Error al guardar: {str(e)}"})
    
    if uploaded_files_info:
        message = f"[{endpoint}] - Archivos guardados exitosamente."
        if errors:
            message += " Algunos archivos tuvieron errores."
        logging.info(message)
        return {
            "mensaje": message,
            "subidos": uploaded_files_info,
            "errores": errors
        }, 200

    return {
        "error": f"[{endpoint}] - No se pudo subir ningún archivo.",
        "errores": errors
    }, 400   


def list_pdf_files(path):
    """Listar los archivos pdf"""
    files = os.listdir(path)
    logging.info(f"Archivos: {files}")
    return [f for f in files if f.endswith(tuple(ALLOWED_EXTENSIONS_chat))]


def entrenar_modelo_tec_ia():
    archivos = list_pdf_files(MODEL_TEC_IA)
    for archivo in archivos:
        process_pdf_files_save_collection(archivo, "TEC-IA")
