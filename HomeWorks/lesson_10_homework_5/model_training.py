from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
from anomaly import detect_anomalies, detect_outliers
from train_and_evaluate_plot_metrics import plot_actual_vs_predicted, plot_scores, plot_feature_importances, plot_residuals

def train_and_evaluate(df):
    # Разделение данных на признаки и целевую переменную
    X = df.drop('Potability', axis=1).values
    y = df['Potability'].values
    
    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Масштабирование данных
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Определение моделей и гиперпараметров
    models = {
        'Linear Regression': (LinearRegression(), {
            'fit_intercept': [True, False]
        }),
        'Random Forest': (RandomForestRegressor(random_state=42), {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30]
        }),
        'Gradient Boosting': (GradientBoostingRegressor(random_state=42), {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        }),
        'SVR': (SVR(), {
            'C': [0.1, 1, 10],
            'gamma': ['scale', 'auto'],
            'kernel': ['linear', 'rbf']
        }),
        'KNN': (KNeighborsRegressor(), {
            'n_neighbors': [3, 5, 7],
            'weights': ['uniform', 'distance']
        })
    }
    
    results = {}
    best_estimators = {}
    y_preds = {}
    
    # Обучение и оценка моделей с настройкой гиперпараметров
    for name, (model, params) in models.items():
        grid_search = GridSearchCV(model, params, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(X_train_scaled, y_train)
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        results[name] = {'MSE': mse, 'R2': r2, 'RMSE': rmse, 'MAE': mae}
        best_estimators[name] = best_model
        y_preds[name] = y_pred
        
        # Обнаружение аномалий для каждой модели
        print(f"Anomalies for {name}:")
        detect_anomalies(X_train_scaled)
        detect_outliers(y_train)
        
        # Визуализация остатков для каждой модели
        plot_residuals(y_test, {name: y_pred})
    
    # Ансамбль моделей (усреднение предсказаний)
    y_pred_ensemble = np.mean([model.predict(X_test_scaled) for model in best_estimators.values()], axis=0)
    y_preds['Ensemble'] = y_pred_ensemble
    results['Ensemble'] = {
        'MSE': mean_squared_error(y_test, y_pred_ensemble),
        'R2': r2_score(y_test, y_pred_ensemble),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_ensemble)),
        'R2': r2_score(y_test, y_pred_ensemble)
    }
    
    # Обнаружение аномалий для ансамбля
    print("Anomalies for Ensemble:")
    detect_anomalies(X_train_scaled)
    detect_outliers(y_train)
    
    # Визуализация остатков для ансамбля
    plot_residuals(y_test, {'Ensemble': y_pred_ensemble})
    
    # Визуализация
    plot_actual_vs_predicted(y_test, y_preds)
    plot_scores(results)
    plot_feature_importances(best_estimators, X)
    
    return results