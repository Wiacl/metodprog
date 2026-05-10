import logging
import os
from pathlib import Path

# Базовый путь к папке с логами
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'

# Создаем папку для логов, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_DIR / 'app.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# Создаем основной логгер
logger = logging.getLogger('courses_catalog')