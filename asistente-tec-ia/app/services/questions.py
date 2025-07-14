import logging
from ollama import generate
from .funciones_auxiliares import convert_format_time
from app.services.files_pdf_process import get_context_from_chroma
from app.services.constants_process import MODEL_TEC_IA, MODEL_CUSTOM_PDF, MODEL_LLAMA

PROMPT_WITH_CONTEXT = """Eres un asistente útil para estudiantes que responde preguntas basándose en el siguiente 
    contexto:{contexto}

    Pregunta: {query}
    Respuesta: """

PROMPT_NO_CONTEXT = """Eres un asistente útil para estudiantes que responde preguntas:
    Pregunta: {query}
    Respuesta:
    """

def generate_answer(prompt):
    try:
        output = generate(
            model="llama3.2",
            prompt=prompt
        )
        min, sec = convert_format_time(output["total_duration"])
        logging.info(f"Respuesta:\nModelo: {str(output['model'])}\nTiempo Total: {str(min)}:{str(sec)}\nRespuesta:{str(output['response'])}\n{str(output['total_duration'])}")
        return output["response"]
    except Exception as e:
        logging.error("Error en el proceso de enviar la pregunta")
        return "Error en el proceso de responder la pregunta"

def get_anwser(query, model_type="TEC-IA"):
    logging.info(f"Procesando pregunta con el modelo {model_type}")

    prompt = PROMPT_NO_CONTEXT.format(query=query)
    contexto = get_context_from_chroma(query, model_type=model_type)

    if contexto:
        prompt = PROMPT_WITH_CONTEXT.format(contexto=contexto, query=query)
        #respuesta = answer_question(prompt)
    return generate_answer(prompt)
