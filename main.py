import mysql.connector
from mysql.connector import Error
import sql_config
import datetime
import os


def create_db_connection(host_name, user_name, user_password, db_name, host_port=None):
    conn = None
    try:
        if host_port is not None:
            conn = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name,
                port=host_port
            )
        else:
            conn = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return conn


def get_table_names(conn, database_name):
    table_names = []
    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {database_name}")
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
        table_names = [row[0] for row in rows]
    except Error as err:
        print(f"Error: '{err}'")
    return table_names


def get_column_names(conn, table_name):
    column_names = []
    try:
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
    except Error as err:
        print(f"Error: '{err}'")
    return column_names

def load_sql_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def creating_import(rows, column_names):
    max_records = 1000
    row_count = 0
    values = ""
    for row in rows:
        row_values = []
        for item in row:
            if item is None:
                row_values.append("NULL")
            elif isinstance(item, str):
                item = item.replace("'", "''")
                row_values.append(f"'{item}'")
            elif isinstance(item, datetime.datetime):
                row_values.append(f"'{item.strftime('%Y-%m-%d %H:%M:%S')}'")
            elif isinstance(item, datetime.date):
                row_values.append(f"'{item.strftime('%Y-%m-%d')}'")
            else:
                row_values.append(str(item))

        values += "(" + ", ".join(row_values) + "), "
        row_count += 1

        if row_count >= max_records:
            values = values[:-2]
            values += f"; \n INSERT INTO `{table_name}` ({', '.join(column_names)}) VALUES "
            row_count = 0

    return values[:-2] + ";"


if 'MYSQL_HOST' in os.environ:
    environment = True
    MYSQL_HOST = os.environ['MYSQL_HOST']
    MYSQL_USER = os.environ['MYSQL_USER']
    MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
    MYSQL_DATABASE = os.environ['MYSQL_DATABASE']
    MYSQL_PORT = os.environ['MYSQL_PORT']
    BACKUP_LIVE = os.environ['BACKUP_LIVE']
    HOST_BACKUP = os.environ['HOST_BACKUP']
    USER_BACKUP = os.environ['USER_BACKUP']
    PASSWORD_BACKUP = os.environ['PASSWORD_BACKUP']
    DATABASE_BACKUP = os.environ['DATABASE_BACKUP']
    PORT_BACKUP = os.environ['PORT_BACKUP']

    connection = create_db_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT)
    database_name = MYSQL_DATABASE
else:
    from sql_config import *
    connection = create_db_connection(sql_config.HOST, sql_config.USER, sql_config.PASSWORD, sql_config.DATABASE, sql_config.PORT)
    database_name = sql_config.DATABASE


if connection is not None:
    cursor = connection.cursor()
    tables = get_table_names(connection, database_name)
    current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
    string = (f'-- Czas generowania: {current_time}\n\n'
              'SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";\n'
              'SET AUTOCOMMIT = 0;\n'
              'START TRANSACTION;\n'
              'SET time_zone = "+00:00";\n'
              '/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n'
              '/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n'
              '/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n'
              '/*!40101 SET NAMES utf8mb4 */;\n\n')

    for table_name in tables:
        column_names = get_column_names(connection, table_name)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            string += f"TRUNCATE TABLE `{table_name}`; \n"
            string += f"INSERT INTO `{table_name}` ({', '.join(column_names)}) VALUES "
            string += creating_import(rows, column_names) + "\n"
        else:
            print(f"No rows found in table '{table_name}', skipping INSERT INTO")

    string += "COMMIT;\n"
    try:
        with open("backup.sql", "w", encoding='utf-8') as file:
            file.write(string)
            print("File backup.sql has been successfully saved.")
    except IOError as err:
        print(f"Error: '{err}'")

    cursor.close()
    connection.close()

    if sql_config.BACKUP_LIVE:
        if environment:
            connection = create_db_connection(HOST_BACKUP, USER_BACKUP, PASSWORD_BACKUP, DATABASE_BACKUP, PORT_BACKUP)
        else:
            connection = create_db_connection(sql_config.HOST_BACKUP, sql_config.USER_BACKUP, sql_config.PASSWORD_BACKUP, sql_config.DATABASE_BACKUP,sql_config.PORT_BACKUP)
        if connection is not None:
            cursor = connection.cursor()
    
            sql_file_path = "backup.sql"
            sql_queries = load_sql_from_file(sql_file_path)
            try:
                cursor.execute(sql_queries, multi=True)
                for result in cursor.stored_results():
                    result.fetchall()
                    connection.commit()
                print("SQL queries successfully executed.")
            except Error as err:
                print(f"Error: {err}")
    
            cursor.close()
            connection.close()
        else:
            print("Unable to establish a database connection.")
else:
    exit()
