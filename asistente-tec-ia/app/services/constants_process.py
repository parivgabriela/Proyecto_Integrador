from chromadb.utils import embedding_functions

DB_DIRECTORY = 'vectordb'
KNOWLEDGE_BASE_PATH = 'app/static/pdfs/'
UPLOAD_USER_PATH = 'uploads'

FAQ_FOLDER = 'data/' # revisar
FAQ_FILE = "faq.json"

uploaded_file_name_bbdd = "BBDD train.pdf"
upload_file_ifts_curricla = "carrera-ifts24-curricula.pdf"

MODEL_TEC_IA = "TEC-IA"
MODEL_CUSTOM_PDF = "CUSTOM-PDF"
MODEL_LLAMA = "LLAMA"

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50