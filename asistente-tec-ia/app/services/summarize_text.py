from transformers import pipeline
import logging
def adaptar_longitud_resumen(texto):
    """
    Ajusta la longitud del resumen según el tamaño del texto original.
    
    Parámetros:
    - texto (str): Texto de entrada.

    Retorna:
    - max_length (int), min_length (int): Parámetros adecuados para la longitud del resumen.
    """
    num_palabras = len(texto.split())

    if 50 < num_palabras <= 150:  # Textos cortos
        return 50, 20  # Resumen breve pero útil
    elif 150 < num_palabras <= 300:  # Textos medianos
        return 100, 40
    elif 300 < num_palabras <= 500:  # Textos medianos
        return 150, 70
    elif 500 < num_palabras <= 1000:  # Textos largos
        return 250, 120
    else:  # Textos muy extensos
        return 0, 0  # supera el limite

def resumir_texto_ai(texto, max_input_words=800):
    """
    Resume un texto en español utilizando modelos de IA como BART.

    Parámetros:
    - texto (str): Texto a resumir.
    - max_input_words (int): Límite de palabras de entrada.

    Retorna:
    - str: Resumen generado por IA.
    """
    modelo_resumidor = pipeline("summarization", model="facebook/bart-large-cnn")

    # Ajusta la longitud del resumen segun su propia long
    max_length, min_length = adaptar_longitud_resumen(texto)
    resumen = modelo_resumidor(texto, max_length=max_length, min_length=min_length, do_sample=False)
    logging.info(f"Maxima longitud del resumen {max_length}")
    return resumen[0]['summary_text']
