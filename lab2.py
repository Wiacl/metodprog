import re

# 1. Валидация логина
def validate_login(login):
    if not login or not login[0].isalpha():
        return False
    if not all(c.isalnum() or c == '_' for c in login):
        return False
    if login[-1] == '_':
        return False
    if len(login) < 5 or len(login) > 20:
        return False
    return True

print("=== 1. Валидация логина ===")
login_input = input("Введите логин для проверки: ")
result = validate_login(login_input)
print(f"Результат: {result}\n")

# 2. Поиск дат в тексте
def find_dates(text):
    pattern = r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b'
    return re.findall(pattern, text)

print("=== 2. Поиск дат в тексте ===")
text_input = input("Введите текст для поиска дат: ")
dates = find_dates(text_input)
print(f"Найденные даты: {dates}\n")

# 3. Парсинг логов
def parse_log(log_line):
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) \w+ user=(\w+) action=(\w+) ip=([\d.]+)'
    match = re.match(pattern, log_line)
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'user': match.group(3),
            'action': match.group(4),
            'ip': match.group(5)
        }
    return None

print("=== 3. Парсинг логов ===")
log_input = input("Введите строку лога (формат: 2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15):\n")
parsed_log = parse_log(log_input)
print(f"Результат парсинга: {parsed_log}\n")

# 4. Проверка пароля
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True

print("=== 4. Проверка пароля ===")
password_input = input("Введите пароль для проверки: ")
password_result = validate_password(password_input)
print(f"Результат проверки пароля: {password_result}\n")

# 5. E-mail с ограниченными доменами
def validate_email_domains(email, domains):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    domain = email.split('@')[-1]
    return domain in domains

print("=== 5. E-mail с ограниченными доменами ===")
domains_list = ['gmail.com', 'yandex.ru', 'edu.ru']
print(f"Допустимые домены: {domains_list}")
email_input = input("Введите email для проверки: ")
email_result = validate_email_domains(email_input, domains_list)
print(f"Результат проверки email: {email_result}\n")

# 6. Нормализация телефонных номеров
def normalize_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 11:
        return f"+7{digits[1:]}"
    elif len(digits) == 10:
        return f"+7{digits}"
    else:
        return None

print("=== 6. Нормализация телефонных номеров ===")
phone_input = input("Введите телефонный номер для нормализации: ")
normalized_phone = normalize_phone(phone_input)
print(f"Нормализованный номер: {normalized_phone}")