import re

STOP_WORDS = {'Город', 'Страна', 'Улица', 'Дом', 'Проспект', 'Пер', 'Переулок', 'Площадь', 'Шоссе', 'Ул', 'Г'}
COMMON_WORDS = {'ученик', 'ученица', 'ученика', 'класса', 'заслуги', 'заслуга', 'отличник'}

def replace_fio(match):
    words = match.groups()

    # Преобразуем в список строк (на случай None и прочих)
    words = [w for w in words if w]

    # Исключаем слова с цифрами или слишком короткие
    if any(len(w) < 3 or any(ch.isdigit() for ch in w) for w in words):
        return match.group()

    # Исключаем общие/школьные слова
    if any(w.lower() in COMMON_WORDS for w in words):
        return match.group()

    # Стоп-слова — например, "Улица Ленина"
    if words[0] in STOP_WORDS:
        return match.group()

    # Убедимся, что все слова с заглавной
    if all(w[0].isupper() for w in words):
        return '[ФИО]'

    return match.group()


    return '[ФИО]'

def anonymize_text(text):
    # ИИН (12 цифр)
    text = re.sub(r'\b\d{12}\b', '[ИИН]', text)

    # Банковская карта (формат 4 группы по 4 цифры с пробелами или без)
    text = re.sub(r'\b(?:\d{4}[ -]?){3}\d{4}\b', '[Карта]', text)

    # Телефон (начинается с +, содержит цифры, пробелы, дефисы)
    text = re.sub(r'(\+?\d[\d\-\s]{7,}\d)', '[Телефон]', text)

    # Email
    text = re.sub(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', '[Email]', text)

    # Адреса (пример: улица Ленина 38, проспект Мира)
    text = re.sub(
        r'\b(?:ул\.?|улица|пр\.?|проспект|пер\.?|переулок|пл\.?|площадь|шоссе|д\.?|дом)\s+[А-Яа-яA-Za-z0-9\- ]+\b',
        '[Адрес]', text, flags=re.IGNORECASE)

    # ФИО из 3 слов
    text = re.sub(r'\b([А-ЯЁ][а-яё]{2,})\s+([А-ЯЁ][а-яё]{2,})\s+([А-ЯЁ][а-яё]{2,})\b', replace_fio, text)

    # ФИО из 2 слов
    text = re.sub(r'\b([А-ЯЁ][а-яё]{2,})\s+([А-ЯЁ][а-яё]{2,})\b', replace_fio, text)

    return text

