import os
import fitz  # PyMuPDF
import re

def anonymize_pdf(pdf_file):
    os.makedirs("outputs", exist_ok=True)

    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    sensitive_patterns = [
        r"\b\d{12}\b",  # ИИН
        r"\b(?:\+?\d[\d\-\s]{7,}\d)\b",  # Телефон
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",  # Email
        r"\b(?:г\.\s?\w+|ул\.\s?\w+|\w+\s?обл\.?)",  # Адреса
        r"\b(?:[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+){1,2})\b",  # ФИО
        r"\b(?:\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b",  # Карты
    ]

    for page in doc:
        blocks = page.get_text("blocks")
        for b in blocks:
            block_text = b[4]
            for pattern in sensitive_patterns:
                for match in re.finditer(pattern, block_text, re.IGNORECASE):
                    x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
                    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=(0, 0, 0), fill=(0, 0, 0))

    output_path = os.path.join("outputs", f"anonymized_{os.path.basename(pdf_file.name)}")
    doc.save(output_path)
    doc.close()
    return output_path 
