import pandas as pd
import re
import nltk
import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_data(df):
    # Оставляем только нужные столбцы и фильтруем строки
    df = df[['target', 'text']].dropna().drop_duplicates()
    df = df[df['target'].isin([0, 4])]

    # Оставляем по 2000 строк с target = 0 и target = 4
    df_0 = df[df['target'] == 0].sample(n=500, random_state=42)
    df_4 = df[df['target'] == 4].sample(n=500, random_state=42)
    df = pd.concat([df_0, df_4])
    
    # Приведение текста к нижнему регистру и удаление знаков препинания
    df['text'] = df['text'].astype(str).str.lower().str.replace(r'[^\w\s]', '', regex=True)
    
    # Удаление часто встречающихся английских слов
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stopwords_eng = set(stopwords.words('english'))
    df['text'] = df['text'].apply(lambda word: " ".join(w for w in word.split() if w not in stopwords_eng))
    
    # Лемматизация
    morph = pymorphy3.MorphAnalyzer()
    df['text'] = df['text'].apply(lambda text: " ".join(morph.parse(word)[0].normal_form for word in text.split()))
    
    # Векторизация TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['text'].fillna(''))
    df['tfidf_vectors'] = list(tfidf_matrix.toarray())
    
    return df