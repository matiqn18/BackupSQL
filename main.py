import mysql.connector
from mysql.connector import Error
import sql_config
import datetime


def create_db_connection(host_name, user_name, user_password, db_name, host_port):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=host_port
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


def creating_import(rows, column_names):
    max_records = 1000
    row_count = 0
    values = ""
    for row in rows:
        values += "("
        for j in range(len(row)):
            if isinstance(row[j], str):
                values += f"'{row[j]}', "
            else:
                values += f"{row[j]}, "

        values = values.rstrip(", ") + "), "
        row_count += 1

        if row_count >= max_records:
            values = values[:-2]
            values += f"; \n INSERT INTO `{table_name}` ({', '.join(column_names)}) VALUES "
            row_count = 0

    return values[:-2]


connection = create_db_connection(sql_config.HOST, sql_config.USER, sql_config.PASSWORD, sql_config.DATABASE, sql_config.PORT)
if connection is not None:
    cursor = connection.cursor()
    tables = get_table_names(connection, sql_config.DATABASE)
    current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
    string = (f'-- Czas generowania: {current_time}\n'
              'SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";\n'
              'SET AUTOCOMMIT = 0;\n'
              'START TRANSACTION;\n'
              'SET time_zone = "+00:00";\n'
              '/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n'
              '/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n'
              '/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n'
              '/*!40101 SET NAMES utf8mb4 */;\n')

    for table_name in tables:
        column_names = get_column_names(connection, table_name)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        string += f"TRUNCATE TABLE `{table_name}`; \n"
        string += f"INSERT INTO `{table_name}` ({', '.join(column_names)}) VALUES "
        string += creating_import(rows, column_names) + "\n"

    string += "COMMIT;\n"
    print(string)
    with open("backup.sql", "w", encoding='utf-8') as file:
        file.write(string)
    cursor.close()
    connection.close()
else:
    exit()
