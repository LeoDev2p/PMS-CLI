import logging

from src.core.setting import BASE_DIR

LOGS_PATH = BASE_DIR / "logs"
LOGS_PATH.mkdir(exist_ok=True)


def get_logger(tipo: str, modulo: str) -> object:
    # error, security, audit
    nombre_completo = f"{tipo}.{modulo}"
    logger = logging.getLogger(nombre_completo)

    if not logger.handlers:
        # 1. Configuración de Formato (Igual para ambos)
        formato_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formato_fecha = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(formato_str, formato_fecha)

        # 2. EL ESCRIBIENTE DE ARCHIVO (FileHandler)
        archivo = BASE_DIR / "logs" / f"{tipo}.log"

        file_handler = logging.FileHandler(archivo)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 3. EL ESCRIBIENTE DE CONSOLA (StreamHandler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 4. NIVEL DE ESCUCHA
        logger.setLevel(logging.INFO)

    return logger
