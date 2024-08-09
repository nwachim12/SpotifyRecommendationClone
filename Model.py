import pandas as pd
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Ensure nltk data is in place
import nltk
nltk.data.path.append('/path/to/nltk_data')  # Update with the path if needed

# Initialize stemmer
stemmer = PorterStemmer()

# Load data
df = pd.read_csv("spotify_millsongdata.csv")

# Data inspection
print(df.head(5))
print(df.tail(5))
print(df.shape)
print(df.isnull().sum())

# Sample and preprocess data
df = df.sample(5000).drop('link', axis=1).reset_index(drop=True)

# Ensure 'text' column is string
df['text'] = df['text'].astype(str)

# Text cleaning
df['text'] = df['text'].replace(r'\r', ' ', regex=True).replace(r'\n', ' ', regex=True).str.lower()

# Tokenization and stemming
def token(txt):
    tokens = nltk.word_tokenize(txt)
    stemmed = [stemmer.stem(w) for w in tokens]
    return " ".join(stemmed)
df['text'] = df['text'].apply(lambda x: token(x))

# TF-IDF and similarity matrix
tfid = TfidfVectorizer(analyzer='word', stop_words='english')
matrix = tfid.fit_transform(df['text'])
sim = cosine_similarity(matrix)

# Save processed data
with open('df.pkl', 'wb') as file:
    pickle.dump(df, file)

with open('similarity.pkl', 'wb') as file:
    pickle.dump(sim, file)

print("Data processing complete. Pickled files saved.")
