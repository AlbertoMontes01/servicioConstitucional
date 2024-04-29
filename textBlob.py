# Importar la biblioteca TextBlob
from textblob import TextBlob
# Crear un objeto TextBlob con una oración
sentence = "TextBlob makes text processing simple."
blob = TextBlob(sentence)
# Obtener la polaridad y subjetividad de la oración
polarity = blob.sentiment.polarity
subjectivity = blob.sentiment.subjectivity
# Imprimir los resultados
print(f"Polarity: {polarity}, Subjectivity: {subjectivity}")
