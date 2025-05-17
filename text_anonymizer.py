import re

STOP_WORDS = {'Город', 'Страна', 'Улица', 'Дом', 'Проспект', 'Пер', 'Переулок', 'Площадь', 'Шоссе', 'Ул', 'Г'}

def replace_fio(match):
    words = match.groups()
    
    words = [w for w in words if w]

    if any(len(w) < 3 or any(ch.isdigit() for ch in w) for w in words):
        return match.group()

    if words[0] in STOP_WORDS:
        return match.group()

    if all(w[0].isupper() for w in words):
        return '[ФИО]'

    return match.group()


    return '[ФИО]'

def anonymize_text(text):
    
    text = re.sub(r'\b\d{12}\b', '[ИИН]', text)

    text = re.sub(r'\b(?:\d{4}[ -]?){3}\d{4}\b', '[Карта]', text)

    text = re.sub(r'(\+?\d[\d\-\s]{7,}\d)', '[Телефон]', text)

    text = re.sub(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', '[Email]', text)

    text = re.sub(
        r'\b(?:ул\.?|улица|пр\.?|проспект|пер\.?|переулок|пл\.?|площадь|шоссе|д\.?|дом)\s+[А-Яа-яA-Za-z0-9\- ]+\b',
        '[Адрес]', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\b([А-ЯЁ][а-яё]{2,})\s+([А-ЯЁ][а-яё]{2,})\s+([А-ЯЁ][а-яё]{2,})\b', replace_fio, text)

    text = re.sub(r'\b([А-ЯЁ][а-яё]{2,})\s+([А-ЯЁ][а-яё]{2,})\b', replace_fio, text)

    return text

