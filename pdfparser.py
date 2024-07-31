from pdfminer.high_level import extract_text

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as f:
        text = extract_text(f)
        return text

