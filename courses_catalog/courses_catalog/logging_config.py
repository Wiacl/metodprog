"""
Конфигурация логирования для проекта
"""
import os
import logging
import logging.handlers
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'

# Создаем папку для логов
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging():
    """Настройка логирования с разными хэндлерами и форматтерами"""
    
    # Создаем форматтер с полной информацией
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)-20s | '
            '%(filename)s:%(lineno)-4d | %(funcName)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Создаем консольный форматтер (более компактный)
    console_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # 1. Консольный хэндлер (StreamHandler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # 2. Файловый хэндлер с ротацией по размеру (RotatingFileHandler)
    # Максимальный размер файла 5 МБ, храним 5 файлов
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_DIR / 'app_rotating.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding='utf-8'
    )
    rotating_file_handler.setLevel(logging.INFO)
    rotating_file_handler.setFormatter(detailed_formatter)
    
    # 3. Файловый хэндлер с ротацией по времени (TimedRotatingFileHandler)
    # Ротация каждый день, храним 7 дней
    timed_file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOG_DIR / 'app_daily.log',
        when='midnight',  # Ротация в полночь
        interval=1,  # Каждый день
        backupCount=7,  # Хранить 7 дней
        encoding='utf-8'
    )
    timed_file_handler.setLevel(logging.DEBUG)
    timed_file_handler.setFormatter(detailed_formatter)
    # Добавляем суффикс с датой к старым файлам
    timed_file_handler.suffix = '%Y-%m-%d'
    
    # 4. Хэндлер для ошибок (только ERROR и выше)
    error_file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_DIR / 'errors.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10,
        encoding='utf-8'
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(detailed_formatter)
    
    # 5. Хэндлер для предупреждений (WARNING и выше)
    warning_file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_DIR / 'warnings.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding='utf-8'
    )
    warning_file_handler.setLevel(logging.WARNING)
    warning_file_handler.setFormatter(detailed_formatter)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Добавляем все хэндлеры к корневому логгеру
    root_logger.addHandler(console_handler)
    root_logger.addHandler(rotating_file_handler)
    root_logger.addHandler(timed_file_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(warning_file_handler)
    
    # Настройка логгера Django (чтобы не дублировать сообщения)
    django_logger = logging.getLogger('django')
    django_logger.setLevel(logging.INFO)
    
    # Настройка логгера для нашего приложения
    app_logger = logging.getLogger('courses_catalog')
    app_logger.setLevel(logging.DEBUG)
    
    # Логгер для users
    users_logger = logging.getLogger('users')
    users_logger.setLevel(logging.DEBUG)
    
    logging.info("=" * 60)
    logging.info("Logging system initialized")
    logging.info(f"Log directory: {LOG_DIR}")
    logging.info(f"Console handler: {'Enabled' if console_handler else 'Disabled'}")
    logging.info(f"Rotating file handler: {rotating_file_handler.baseFilename}")
    logging.info(f"Timed file handler: {timed_file_handler.baseFilename}")
    logging.info(f"Error file handler: {error_file_handler.baseFilename}")
    logging.info(f"Warning file handler: {warning_file_handler.baseFilename}")
    logging.info("=" * 60)
    
    return root_logger