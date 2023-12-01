// Importar la biblioteca natural y crear un tokenizador de palabras
const natural = require('natural');
const tokenizer = new natural.WordTokenizer();
// Definir una oración
const sentence = "NLTK is powerful!";
// Tokenizar la oración
const words = tokenizer.tokenize(sentence);
// Imprimir las palabras tokenizadas
console.log(words);
