import pandas as pd
import re
import nltk
import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_data(df):
    # определение столбцов с пропущенными значениями 
    missing_columns = df.columns[df.isnull().any()]
    
    # Для некатегориальных столбцов (числовых) с пропущенными значениями заменяем пропущенные средними
    # а для категориальных - на наиболее часто встречающиеся значения (моду)
    for column in missing_columns:
        if df[column].dtype != 'object':
            df[column] = df[column].fillna(df[column].mean())
        else:
            df[column] = df[column].fillna(df[column].mode()[0])
    
    return df