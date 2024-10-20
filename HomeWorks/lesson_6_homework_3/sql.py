import psycopg2
from config import DB_CONFIG

def select_data():
    conn = psycopg2.connect(
        dbname=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )
    cur = conn.cursor()

    # Пример 1: Извлечение всех астронавтов из определенной страны
    query1 = """
    SELECT name_dictionary.name, country_dictionary.country
    FROM main_table
    JOIN name_dictionary ON main_table.name_id = name_dictionary.name_id
    JOIN country_dictionary ON main_table.country_id = country_dictionary.country_id
    WHERE country_dictionary.country = 'USA';
    """
    cur.execute(query1)
    result1 = cur.fetchall()
    print("Астронавты из USA:", result1)
    print()  # Пустая строка

    # Пример 2: Извлечение всех астронавтов, совершивших более 5 полетов
    query2 = """
    SELECT name_dictionary.name, main_table.total_flights
    FROM main_table
    JOIN name_dictionary ON main_table.name_id = name_dictionary.name_id
    WHERE main_table.total_flights > 5;
    """
    cur.execute(query2)
    result2 = cur.fetchall()
    print("Астронавты с более чем 5 полетами:", result2)
    print()  # Пустая строка

    # Пример 3: Подсчет общего количества астронавтов
    query3 = """
    SELECT COUNT(*) AS total_astronauts
    FROM main_table;
    """
    cur.execute(query3)
    result3 = cur.fetchone()
    print("Общее количество астронавтов:", result3[0])
    print()  # Пустая строка

    # Пример 4: Подсчет общего количества полетов всех астронавтов
    query4 = """
    SELECT SUM(total_flights) AS total_flights
    FROM main_table;
    """
    cur.execute(query4)
    result4 = cur.fetchone()
    print("Общее количество полетов:", result4[0])
    print()  # Пустая строка

    # Пример 5: Среднее количество полетов на одного астронавта
    query5 = """
    SELECT AVG(total_flights) AS average_flights
    FROM main_table;
    """
    cur.execute(query5)
    result5 = cur.fetchone()
    print("Среднее количество полетов на одного астронавта:", result5[0])

    cur.close()
    conn.close()

if __name__ == "__main__":
    select_data()