from transformers import pipeline
import logging
import nltk
import ollama

try:
    # Intenta encontrar el recurso 'punkt'
    nltk.data.find('tokenizers/punkt')
    logging.info("El recurso 'punkt' de NLTK ya está descargado.")
except LookupError:
    # Si no lo encuentra, lo descarga.
    logging.info("Descargando el recurso 'punkt' de NLTK...")
    nltk.download('punkt')
    nltk.download('punkt_tab')

def resumir_texto_llama3(text: str, modelo_ollama: str = "llama3.2:latest", max_tokens_por_bloque: int = 2000) -> str:
    """
    Parámetros:
    - text (str): El texto en español a resumir
    - modelo_ollama (str): El nombre del modelo de Llama 3.2 debe estar instalado, ejecutar ollama list para ver los modelos que se tiene en el sistema.
    - max_tokens_por_bloque (int): Número máximo de tokens aproximado para cada bloque de texto a procesar.

    Retorna:
    - str: El resumen generado, o un mensaje de error si no se pudo procesar.
    """
    if not text or len(text.strip()) < 50: # Un mínimo de palabras para que valga la pena resumir
        logging.warning("El texto es demasiado corto para ser resumido o está vacío.")
        return text.strip() if text else "No se pudo generar un resumen para el text proporcionado (texto muy corto)."

    oraciones = nltk.sent_tokenize(text, language='spanish')
    
    bloques = []
    bloque_actual_oraciones = []
    longitud_actual_palabras = 0

    max_palabras_por_bloque = int(max_tokens_por_bloque / 1.3)
    
    for oracion in oraciones:
        longitud_oracion_palabras = len(oracion.split())
        
        if (longitud_actual_palabras + longitud_oracion_palabras) <= max_palabras_por_bloque:
            bloque_actual_oraciones.append(oracion)
            longitud_actual_palabras += longitud_oracion_palabras
        else:
            if bloque_actual_oraciones:
                bloques.append(" ".join(bloque_actual_oraciones))
            bloque_actual_oraciones = [oracion]
            longitud_actual_palabras = longitud_oracion_palabras
    
    if bloque_actual_oraciones:
        bloques.append(" ".join(bloque_actual_oraciones))

    if not bloques: # Si el texto era muy corto o no se pudo dividir
        bloques.append(text)

    resumenes_parciales = []
    for i, bloque in enumerate(bloques):
        logging.info(f"Procesando bloque {i+1}/{len(bloques)} con aproximadamente {len(bloque.split())} palabras.")
        
        # El "prompt" es crucial para guiar al modelo
        prompt = f"Por favor, resume el siguiente texto en español de manera concisa y clara:\n\n{bloque}\n\nResumen:"
        
        try:
            num_predicciones_deseadas = max(100, int(len(bloque.split()) * 0.25))

            response = ollama.generate(
                model=modelo_ollama, 
                prompt=prompt,
                options={
                    'num_predict': num_predicciones_deseadas,
                    'temperature': 0.5 # Ajusta para más creatividad (alto) o más concisión (bajo)
                }
            )
            
            summary_text = response['response'].strip()
            if summary_text:
                resumenes_parciales.append(summary_text)
            else:
                logging.warning(f"El bloque {i+1} no generó un resumen. Respuesta vacía del modelo.")

        except Exception as e:
            logging.error(f"Error al llamar a Ollama para el bloque {i+1}: {e}")
            resumenes_parciales.append(f"Error al resumir el bloque {i+1}.")

    if not resumenes_parciales:
        return "No se pudo generar un resumen para el texto proporcionado."
    
    # Si hay varios resúmenes parciales, combinarlos y resumir el resultado si es necesario
    resumen_combinado = " ".join(resumenes_parciales)
    
    # Si el resumen combinado es todavía muy largo, hacer un resumen final de los resúmenes parciales
    if len(resumen_combinado.split()) > (max_tokens_por_bloque / 2): # Si el combinado es más de la mitad del bloque original
        logging.info("Realizando un resumen final de los resúmenes parciales combinados.")
        prompt_final = f"Los siguientes son resúmenes de diferentes secciones de un texto. Por favor, combínalos en un resumen final y coherente en español:\n\n{resumen_combinado}\n\nResumen final:"
        try:
            response_final = ollama.generate(
                model=modelo_ollama, 
                prompt=prompt_final,
                options={
                    'num_predict': max(200, int(len(resumen_combinado.split()) * 0.3)), # Limita la longitud del resumen final
                    'temperature': 0.6
                }
            )
            resumen_final = response_final['response'].strip()
            return resumen_final if resumen_final else "No se pudo generar un resumen final coherente."
        except Exception as e:
            logging.error(f"Error al generar el resumen final: {e}")
            return "Se generaron resúmenes parciales, pero hubo un error al combinarlos en un resumen final." + resumen_combinado
    
    return resumen_combinado
