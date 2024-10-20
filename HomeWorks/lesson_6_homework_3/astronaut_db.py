import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from requests.exceptions import RequestException
from config import DB_CONFIG

# Подключение к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Успешное подключение к базе данных")
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise

# Функция для создания таблиц
def create_tables(conn):
    try:
        cur = conn.cursor()

        # Создание таблицы name_dictionary
        cur.execute("""
            CREATE TABLE IF NOT EXISTS name_dictionary (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                name_id INT NOT NULL UNIQUE
            );
        """)
        print("Таблица name_dictionary создана")

        # Создание таблицы country_dictionary
        cur.execute("""
            CREATE TABLE IF NOT EXISTS country_dictionary (
                id SERIAL PRIMARY KEY,
                country VARCHAR(100) NOT NULL,
                country_id INT NOT NULL UNIQUE
            );
        """)
        print("Таблица country_dictionary создана")

        # Создание таблицы gender_dictionary
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gender_dictionary (
                id SERIAL PRIMARY KEY,
                gender VARCHAR(100) NOT NULL,
               gender_id INT NOT NULL UNIQUE
            );
        """)
        print("Таблица gender_dictionary создана")
        
        # Создание таблицы flights_dictionary
        cur.execute("""
            CREATE TABLE IF NOT EXISTS flights_dictionary (
                id SERIAL PRIMARY KEY,
                flights VARCHAR(100) NOT NULL,
                flights_id INT NOT NULL UNIQUE
            );
        """)
        print("Таблица flights_dictionary создана")

        # Создание главной таблицы о полетах аcтронавтов
        cur.execute("""
            CREATE TABLE IF NOT EXISTS main_table (
            id SERIAL PRIMARY KEY,
            name_id INT NOT NULL,
            country_id INT NOT NULL,
            gender_id INT NOT NULL,
            flights_id INT NOT NULL,
            total_flights INT NOT NULL,
            total_flight_time TEXT NOT NULL,
            year INT NOT NULL,
            FOREIGN KEY (name_id) REFERENCES name_dictionary(name_id),
            FOREIGN KEY (country_id) REFERENCES country_dictionary(country_id),
            FOREIGN KEY (gender_id) REFERENCES gender_dictionary(gender_id),
            FOREIGN KEY (flights_id) REFERENCES flights_dictionary(flights_id)
            );
        """)
        print("Таблица main_table создана")

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
        conn.rollback()
        raise


# Функция импорта данных name_dictionary
def import_data_name_dictionary(conn, df):
    try:
        cur = conn.cursor()

        name_dictionary_values = [
            (row['Name'], row['Index'])
            for _, row in df.iterrows()
        ]
        execute_values(cur, """
            INSERT INTO name_dictionary (name, name_id)
            VALUES %s
            ON CONFLICT (name_id) DO NOTHING;
        """, name_dictionary_values)
        print("Данные name_dictionary импортированы")

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при импорте данных: {e}")
        conn.rollback()
        raise

# Функция импорта данных country_dictionary
def import_data_country_dictionary(conn, df):
    try:
        cur = conn.cursor()

        country_dictionary_values = [
            (row['Country'], row['Index'])
            for _, row in df.iterrows()
        ]
        execute_values(cur, """
            INSERT INTO country_dictionary (country, country_id)
            VALUES %s
            ON CONFLICT (country_id) DO NOTHING;
        """, country_dictionary_values)
        print("Данные country_dictionary импортированы")

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при импорте данных: {e}")
        conn.rollback()
        raise

# Функция импорта данных gender_dictionary
def import_data_gender_dictionary(conn, df):
    try:
        cur = conn.cursor()

        gender_dictionary_values = [
            (row['Gender'], row['Index'])
            for _, row in df.iterrows()
        ]
        execute_values(cur, """
            INSERT INTO gender_dictionary (gender, gender_id)
            VALUES %s
            ON CONFLICT (gender_id) DO NOTHING;
        """, gender_dictionary_values)
        print("Данные gender_dictionary импортированы")

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при импорте данных: {e}")
        conn.rollback()
        raise

# Функция импорта данных flights_dictionary
def import_data_flights_dictionary(conn, df):
    try:
        cur = conn.cursor()

        flights_dictionary_values = [
            (row['Flights'], row['Index'])
            for _, row in df.iterrows()
        ]
        execute_values(cur, """
            INSERT INTO flights_dictionary (flights, flights_id)
            VALUES %s
            ON CONFLICT (flights_id) DO NOTHING;
        """, flights_dictionary_values)
        print("Данные flights_dictionary импортированы")

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при импорте данных: {e}")
        conn.rollback()
        raise

# Функция импорта данных о полетах аcтронавтов
def import_data_main_table(conn, df):
    try:
        cur = conn.cursor()

        astronauts_values = [
            (row['Name'], row['Country'], row['Gender'], row['Flights'], row['Total Flights'],
             row['Total Flight Time (ddd:hh:mm)'], row['Year'])
            for _, row in df.iterrows()
        ]
        execute_values(cur, """
            INSERT INTO main_table (name_id, country_id, gender_id, flights_id, total_flights, 
                                  total_flight_time, year)
            VALUES %s;
            """, astronauts_values)
        print("Данные о полетах аcтронавтов импортированы")

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при импорте данных: {e}")
        conn.rollback()
        raise