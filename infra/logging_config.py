# logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        filename='application.log',  # Salva os logs em um arquivo
        level=logging.INFO,  # Define o nível mínimo de severidade para capturar
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato customizado para as mensagens de log
        datefmt='%Y-%m-%d %H:%M:%S',  # Formato de data/hora
    )

    # Configura um handler adicional para saída no console com nível WARNING ou superior
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console_handler)
