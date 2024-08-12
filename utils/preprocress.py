from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import os

nltk_data_path = '/root/nltk_data'
if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers/punkt')):
    nltk.download('punkt')
if not os.path.exists(os.path.join(nltk_data_path, 'stopwords')):
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens
