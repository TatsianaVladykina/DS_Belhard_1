import psycopg2
from config import DB_CONFIG
import matplotlib.pyplot as plt
import seaborn as sns

def select_data(query):
    conn = psycopg2.connect(
        dbname=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def plot_astronauts_with_more_than_5_flights():
    query = """
    SELECT name_dictionary.name, main_table.total_flights
    FROM main_table
    JOIN name_dictionary ON main_table.name_id = name_dictionary.name_id
    WHERE main_table.total_flights > 5;
    """
    data = select_data(query)
    names, flights = zip(*data)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(flights), y=list(names))
    plt.title('Астронавты, совершившие более пяти полетов')
    plt.xlabel('Total Flights')
    plt.ylabel('Astronaut Name')
    plt.tight_layout()
    plt.show()

def plot_top_5_astronauts_by_country():
    query = """
    SELECT country_dictionary.country, COUNT(main_table.id) as astronaut_count
    FROM main_table
    JOIN country_dictionary ON main_table.country_id = country_dictionary.country_id
    GROUP BY country_dictionary.country
    ORDER BY astronaut_count DESC
    LIMIT 5;
    """
    data = select_data(query)
    countries, counts = zip(*data)
    
    plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=countries, autopct='%1.1f%%', startangle=140)
    plt.title('Топ 5 стран по количеству астронавтов')
    plt.axis('equal')
    plt.show()


def plot_astronauts_by_gender():
    query = """
    SELECT gender_dictionary.gender, COUNT(main_table.id) as astronaut_count
    FROM main_table
    JOIN gender_dictionary ON main_table.gender_id = gender_dictionary.gender_id
    GROUP BY gender_dictionary.gender;
    """
    data = select_data(query)
    genders, counts = zip(*data)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(genders), y=list(counts))
    plt.title('Распределение астронавтов по полу')
    plt.xlabel('Пол')
    plt.ylabel('Количество астронавтов')
    plt.tight_layout()
    plt.show()

