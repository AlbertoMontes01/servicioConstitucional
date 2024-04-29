import os
import string
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

# Define the path to your existing PDF file
pdf_file_path = r'C:\Users\alber\Desktop\quijote.pdf'  # Replace with the actual path to your PDF file using raw string literal (r'')

# Extract text from the PDF file
pdf_text = []
with open(pdf_file_path, 'rb') as pdf_file:
    pdf_reader = PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        # Extract text from the page and handle any decoding errors
        try:
            page_text = page.extract_text()
        except Exception as e:
            print(f"Error extracting text from page {page_num + 1}: {e}")
            page_text = ""
        pdf_text.append(page_text)

# Preprocess the extracted text
cleaned_texts = []
for text in pdf_text:
    # Convert text to lowercase
    text_lower = text.lower()
    # Remove punctuation characters
    text_no_punct = ''.join([c for c in text_lower if c not in string.punctuation])
    # Remove digits
    text_no_digits = ''.join([c for c in text_no_punct if not c.isdigit()])
    # Remove extra whitespace and split into words
    clean_text = ' '.join(text_no_digits.split())
    cleaned_texts.append(clean_text)

# Plot histogram of text lengths
text_lengths = [len(text.split()) for text in cleaned_texts if text.strip()]  # Filter out empty texts
text_lengths = [length for length in text_lengths if length < 50]  # Filter out very long texts
plt.hist(text_lengths, bins=25)
plt.title('Histogram of Number of Words in Texts')
plt.xlabel('Number of Words')
plt.ylabel('Frequency')
plt.show()
