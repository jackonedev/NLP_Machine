from nltk.tokenize import WhitespaceTokenizer
### no me gusta
texto = "Este es un ejemplo de tokenizador basado!! en espacios en blanco."
tokenizer = WhitespaceTokenizer()
tokens = tokenizer.tokenize(texto)
### no me gusta

print(tokens)




#######################################################################

from nltk.tokenize import word_tokenize

texto = "Este es otro ejemplo de tokenizadorrrrr basado!! en palabras."
tokens = word_tokenize(texto)

print(tokens)