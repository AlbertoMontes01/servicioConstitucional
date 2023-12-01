import PyPDF2
from tkinter import Tk, filedialog


def pdf_to_text(pdf_path):
    text = ""

    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

    return text


def select_pdf():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    return file_path


# Seleccionar el archivo PDF
pdf_path = select_pdf()

if pdf_path:
    # Convertir el PDF a texto
    text_content = pdf_to_text(pdf_path)

    # Guardar el contenido de texto en un archivo TXT
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if save_path:
        with open(save_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_content)