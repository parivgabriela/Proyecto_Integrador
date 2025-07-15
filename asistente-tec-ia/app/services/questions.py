import logging
from ollama import generate
from .funciones_auxiliares import convert_format_time
from app.services.files_pdf_process import get_context_from_chroma
from app.services.constants_process import MODEL_LLM

PROMPT_WITH_CONTEXT = """Eres un asistente experto encargado de responder preguntas basándote ÚNICAMENTE en un contexto específico.
    Tu tarea es leer el contexto y la pregunta, y luego formular una respuesta clara y concisa utilizando solo la información proporcionada.
    Basa tu respuesta solamente con los datos del contexto. Si la información del contexto no es suficiente para responder la pregunta de manera definitiva, responde exactamente con: "No encontré información sobre eso en el documento." No intentes adivinar ni usar conocimiento externo.
    ---CONTEXTO---
    {contexto}
    ---PREGUNTA---
    {query}
    ---RESPUESTA---
"""

PROMPT_NO_CONTEXT = """
    Eres un asistente académico experto, especializado en Programacion en python, Inteligencia de negocios, Ciencia de Datos e Inteligencia Artificial. Tu audiencia son estudiantes universitarios de esta carrera.
    Tu objetivo es responder a la pregunta del estudiante siguiendo estas reglas estrictamente:

    1.  **Claridad y Precisión**: Responde de manera clara y conceptualmente correcta. Usa la terminología técnica adecuada, pero explícala de forma sencilla.
    2.  **Concisión**: Sé breve y ve al punto. Evita la historia del concepto, las introducciones largas o la información extra no solicitada. Una definición y un ejemplo simple suelen ser suficientes.
    3.  **Evitar Alucinaciones**: Basa tu respuesta únicamente en conocimiento bien establecido en el campo de la ciencia de datos y la IA. Si la pregunta es ambigua o no tienes una respuesta factual y verificable, responde con: "No puedo proporcionar una respuesta precisa sobre ese tema."
---
**Pregunta:** {query}

**Respuesta Directa y Concisa:**
"""


def generate_answer(prompt):
    try:
        output = generate(
            model=MODEL_LLM,
            prompt=prompt
        )
        min, sec = convert_format_time(output["total_duration"])
        logging.info(f"Respuesta:\nModelo: {str(output['model'])}\nTiempo Total: {str(min)}:{str(sec)}\nRespuesta:{str(output['response'])}\n{str(output['total_duration'])}")
        return output["response"]
    except Exception as e:
        logging.error(f"Error en el proceso de enviar la pregunta {prompt}")
        return "Error en el proceso de responder la pregunta"

def get_anwser(query, model_type="TEC-IA"):
    logging.info(f"Procesando pregunta con el modelo {model_type}")

    prompt = PROMPT_NO_CONTEXT.format(query=query)
    contexto = get_context_from_chroma(query, model_type=model_type)

    if contexto:
        prompt = PROMPT_WITH_CONTEXT.format(contexto=contexto, query=query)

    return generate_answer(prompt)
