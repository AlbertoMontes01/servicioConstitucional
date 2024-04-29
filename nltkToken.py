#Importar la biblioteca NLTK y descargar el tokenizador de palabras
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
# Definir una oración
sentence = "NLTK is powerful!"
# Tokenizar la oración
words = word_tokenize(sentence)
# Imprimir las palabras tokenizadas
print(words)
