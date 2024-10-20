import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

def analyze_distribution(df):
   # Определение числовых и категориальных признаков
    numerical_features = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # Гистограммы числовых признаков
    df[numerical_features].hist(bins=15, figsize=(15, 10), layout=(len(numerical_features) // 3 + 1, 3))
    plt.suptitle('Histograms of Numerical Features')
    plt.show()
    
    # Pairplot числовых признаков по potability
    if 'Potability' in df.columns:
        sns.pairplot(df, hue='Potability', vars=numerical_features)
        plt.suptitle('Pairplot of Numerical Features by Potability', y=1.02)
        plt.show()
    
    # Корреляционная тепловая карта
    plt.figure(figsize=(12, 8))
    corr_matrix = df[numerical_features].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.show()
    
    # Boxplots числовых признаков
    plt.figure(figsize=(15, 10))
    for i, feature in enumerate(numerical_features):
        plt.subplot(len(numerical_features) // 3 + 1, 3, i + 1)
        sns.boxplot(x='Potability', y=feature, data=df)
        plt.title(f'Boxplot of {feature}')
    plt.suptitle('Boxplots of Numerical Features')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    
