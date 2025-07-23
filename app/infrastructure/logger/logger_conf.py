import logging
import os
import sys

def setup_global_config_logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler(sys.stdout),
                        ]
)

name_level = {
    "domain":"app/infrastructure/logger/logs/domain.log",
    "application":"app/infrastructure/logger/logs/application.log",
    "api":"app/infrastructure/logger/logs/api.log",
    "infrastructure":"app/infrastructure/logger/logs/infrastructure.log",
    "celery_app":"app/infrastructure/logger/logs/celery_app.log",
    "tests":"app/infrastructure/logger/logs/tests.log",
}

def get_logger(name: str, file_path: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # або LOGGER_LEVEL, якщо він є

    log_path = name_level.get(file_path)
    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)  # створює директорії, якщо не існують

        # Перевірка, щоб не додати дубльований FileHandler
        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_path) for h in logger.handlers):
            fh = logging.FileHandler(log_path, encoding='utf-8')
            fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(fh)

    return logger