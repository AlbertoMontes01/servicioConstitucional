# Importing Lemmatizer library from nltk
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 
 
print('rocks :', lemmatizer.lemmatize('rocks')) 
print('corpora : ', lemmatizer.lemmatize('corpora'))
