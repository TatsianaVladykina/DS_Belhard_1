import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detect_anomalies(features):
    # Стандартизация признаков
    scaler_IF = StandardScaler()
    X_scaled_IF = scaler_IF.fit_transform(features)

    # Построение модели Isolation Forest
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X_scaled_IF)
    y_pred_IF = clf.predict(X_scaled_IF)

    # Отображение результатов
    plt.title("Isolation Forest для обнаружения аномалий")
    plt.scatter(X_scaled_IF[:, 0], X_scaled_IF[:, 1], c='white', s=20, edgecolor='k')

    # Отображение нормальных точек
    normal_points_IF = X_scaled_IF[y_pred_IF == 1]
    plt.scatter(normal_points_IF[:, 0], normal_points_IF[:, 1], c='blue', s=20, edgecolor='k', label="Нормальные точки")

    # Отображение аномалий
    anomalies_IF = X_scaled_IF[y_pred_IF == -1]
    plt.scatter(anomalies_IF[:, 0], anomalies_IF[:, 1], c='red', s=20, edgecolor='k', label="Аномалии")

    plt.legend()
    plt.show()

def detect_outliers(target):
    # Вычисление Z-оценок
    mean_Z = np.mean(target)
    std_dev_Z = np.std(target)
    z_scores = [(x - mean_Z) / std_dev_Z for x in target]

    # Определение порога для выбросов
    threshold = 3

    # Поиск выбросов
    outliers = np.where(np.abs(z_scores) > threshold)

    # Визуализация данных и выбросов
    plt.figure(figsize=(10, 6))
    plt.plot(target, 'bo', label='Данные')
    plt.plot(outliers[0], np.array(target)[outliers], 'ro', label='Выбросы')
    plt.axhline(mean_Z, color='g', linestyle='dashed', linewidth=2, label='Среднее значение')
    plt.axhline(mean_Z + threshold * std_dev_Z, color='r', linestyle='dotted', linewidth=2, label='Порог выбросов')
    plt.axhline(mean_Z - threshold * std_dev_Z, color='r', linestyle='dotted', linewidth=2)

    plt.title('Обнаружение выбросов с использованием Z-Score')
    plt.xlabel('Индекс')
    plt.ylabel('Значение')
    plt.legend()
    plt.show()

    # Вывод найденных выбросов
    print("Найденные выбросы:", np.array(target)[outliers])