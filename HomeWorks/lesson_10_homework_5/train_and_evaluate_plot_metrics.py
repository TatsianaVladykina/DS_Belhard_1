import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def plot_actual_vs_predicted(y_test, y_preds):
    plt.figure(figsize=(10, 6))
    for name, y_pred in y_preds.items():
        plt.scatter(range(len(y_test)), y_test, color='green', label='Фактические значения')
        plt.scatter(range(len(y_test)), y_pred, color='pink', label=f'Предсказанные значения - {name}')
        plt.xlabel('Наблюдение')
        plt.ylabel('Значение')
        plt.title(f'Фактические и предсказанные значения - {name}')
        plt.legend()
        plt.show()

def plot_scores(results):
    # Преобразование словаря результатов в DataFrame
    metrics_df = pd.DataFrame(results).T
    
    # Проверка наличия всех метрик
    required_metrics = ['MSE', 'R2', 'RMSE', 'MAE']
    for metric in required_metrics:
        if metric not in metrics_df.columns:
            metrics_df[metric] = np.nan  # Добавление столбца с NaN, если метрика отсутствует
    
    # Построение графика
    metrics_df.plot(kind='bar', figsize=(10, 6))
    plt.title('MAE, MSE, RMSE и R2 для каждой модели')
    plt.xlabel('Модель')
    plt.ylabel('Значение')
    plt.tight_layout()
    plt.show()

def plot_feature_importances(best_estimators, X):
    # Преобразование X в DataFrame, если это numpy.ndarray
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
    
    feature_importances = pd.DataFrame()
    for name, model in best_estimators.items():
        if hasattr(model, 'feature_importances_'):
            feature_importances[name] = model.feature_importances_
        elif hasattr(model, 'coef_'):
            feature_importances[name] = model.coef_
        else:
            feature_importances[name] = [0] * X.shape[1]  # Заполнение нулями, если атрибут отсутствует
    
    # Добавление важности признаков для ансамбля
    ensemble_importances = feature_importances.mean(axis=1)
    feature_importances['Ensemble'] = ensemble_importances
    
    feature_importances.index = X.columns
    feature_importances.plot(kind='bar', figsize=(10, 6))
    plt.title('Важность признаков для каждой модели')
    plt.xlabel('Признак')
    plt.ylabel('Важность')
    plt.tight_layout()
    plt.show()

def plot_residuals(y_test, y_preds):
    for name, y_pred in y_preds.items():
        residuals = y_test - y_pred
        plt.figure(figsize=(8, 6))
        sns.histplot(residuals, kde=True, bins=30, color='orange')
        plt.title(f'Распределение остатков - {name}')
        plt.xlabel('Остаток (Target - Предсказание)')
        plt.ylabel('Частота')
        plt.show()
        
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=y_pred, y=residuals, color='green', alpha=0.6)
        plt.axhline(0, color='red', linestyle='--')
        plt.xlabel('Предсказанные значения')
        plt.ylabel('Остатки')
        plt.title(f'Остатки vs Предсказанные значения - {name}')
        plt.show()