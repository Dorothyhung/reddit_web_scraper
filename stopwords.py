import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer


sent = "I will walk 500 miles and I would walk 500 more, just to be the man who walks a thousand miles to fall down at your door!"
stop_words = stopwords.words('english')

token = word_tokenize(sent)
cleaned_token = []
for word in token:
    if word not in stop_words:
        cleaned_token.append(word)
        
stemmer = PorterStemmer()
stemmed = [stemmer.stem(word) for word in cleaned_token]

print("This is the unclean version:", token)
print("This is the cleaned version:", stemmed)
