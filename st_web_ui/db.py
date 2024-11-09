import sqlite3
import csv
import pandas as pd
from typing import Dict

class SQLiteManager:
    def __init__(self, db_name: str):
        """
        Инициализация менеджера базы данных с заданным именем базы данных.
        При инициализации создается база данных и таблица, если они не существуют.

        Аргументы:
            db_name (str): Имя файла базы данных.
        """
        self.db_name = db_name
        self._create_db_and_table()

    def _create_db_and_table(self):
        """
        Создает базу данных и таблицу 'tasks', если они еще не существуют.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Создание схемы таблицы с указанными столбцами
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tasks (
            created_at TEXT,
            status TEXT,
            device TEXT,
            failure_point TEXT,
            serial_number TEXT,
            topic TEXT,
            description TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def init_db_from_csv(self, csv_file: str):
        """
        Инициализирует базу данных путем загрузки данных из CSV файла.
        Загрузка осуществляется только для выбранных столбцов.

        Аргументы:
            csv_file (str): Путь к CSV файлу.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Определяем столбцы, которые необходимо извлечь из CSV файла
        desired_columns = ['created_at', 'status', 'Тип оборудования', 'Точка отказа',
                           'Серийный номер', 'Тема', 'Описание']
        
        # Маппинг столбцов CSV на столбцы базы данных
        column_mapping = {
            'created_at': 'created_at',
            'status': 'status',
            'Тип оборудования': 'device',
            'Точка отказа': 'failure_point',
            'Серийный номер': 'serial_number',
            'Тема': 'topic',
            'Описание': 'description'
        }
        
        # Чтение CSV и вставка только нужных столбцов в базу данных
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Извлекаем необходимые данные на основе маппинга столбцов
                extracted_data = {db_col: row[csv_col] for csv_col, db_col in column_mapping.items() if csv_col in row}
                
                cursor.execute(''' 
                INSERT INTO tasks (created_at, status, device, failure_point, serial_number, topic, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    extracted_data['created_at'], extracted_data['status'], extracted_data['device'],
                    extracted_data['failure_point'], extracted_data['serial_number'],
                    extracted_data['topic'], extracted_data['description']
                ))
        
        conn.commit()
        conn.close()

    def add_row(self, data: Dict):
        """
        Добавляет новую строку в таблицу 'tasks'.

        Аргументы:
            data (Dict): Данные для добавления в таблицу. Ожидается, что в словаре будут ключи:
                         'created_at', 'status', 'device', 'failure_point', 'serial_number', 'topic', 'description'.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(''' 
        INSERT INTO tasks (created_at, status, device, failure_point, serial_number, topic, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['created_at'], data['status'], data['device'], data['failure_point'], 
              data['serial_number'], data['topic'], data['description']))
        
        conn.commit()
        conn.close()

    def fetch_all(self):
        """
        Извлекает все строки из таблицы 'tasks'.

        Возвращает:
            list: Список всех строк из таблицы.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        
        conn.close()
        return rows

    def load_to_dataframe(self) -> pd.DataFrame:
        """
        Загружает содержимое таблицы 'tasks' в pandas DataFrame.

        Возвращает:
            pd.DataFrame: DataFrame с данными из таблицы 'tasks'.
        """
        conn = sqlite3.connect(self.db_name)
        query = "SELECT * FROM tasks"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
