import logging

def convert_format_time(total_time):
    try:
        total_duration_us = int(total_time)
        total_seconds = total_duration_us / 1_000_000_000

        minutes = int(total_seconds // 60)

        # Obtener los segundos restantes
        seconds = int(total_seconds % 60)
        return minutes, seconds
    except Exception as e:
        logging.error(f"Error de conversion {e}")
    logging.info(f"Duración total: {minutes} minutos y {seconds} segundos")