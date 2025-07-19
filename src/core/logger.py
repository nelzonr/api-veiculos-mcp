
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Configuração do diretório de logs
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)

def setup_logger(name=__name__):
    """Configura um logger com rotação de arquivos"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Captura todos os níveis
    
    # Formato padrão
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (rotação a cada 10MB, mantém 5 backups)
    file_handler = RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Remove handlers existentes (evita duplicação)
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger("app")