import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

def analyze_distribution(df):
    # Определение числовых столбцов
    numerical_columns = ['target','id']
    
    # Построение гистограмм для каждого числового признака
    plt.figure(figsize=(16, 12))
    for i, column in enumerate(numerical_columns, 1):
        plt.subplot(4, 4, i)
        sns.histplot(df[column], kde=True, color='c')
        plt.title(f'{column} distribution')
    plt.tight_layout()
    plt.show()

    # Вычисление асимметрии (skewness) и эксцесса (kurtosis)
    skewness_kurtosis = {
        "Feature": [],
        "Skewness": [],
        "Kurtosis": []
    }

    for column in numerical_columns:
        skewness_kurtosis["Feature"].append(column)
        skewness_kurtosis["Skewness"].append(skew(df[column]))
        skewness_kurtosis["Kurtosis"].append(kurtosis(df[column]))
    
    # Преобразование в DataFrame для удобства
    result_df = pd.DataFrame(skewness_kurtosis)
    return result_df