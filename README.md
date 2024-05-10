# BackupSQL

BackupSQL is a Python script for creating SQL backups of MySQL databases. It connects to a MySQL database, retrieves table names and column names, and exports the data to a SQL file for backup purposes.

## Features

- Connects to a MySQL database using specified credentials.
- Retrieves table names and column names from the connected database.
- Generates SQL queries to export table data.
- Saves the SQL backup to a file.

## Installation

To use BackupSQL, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/BackupSQL.git
```

2. Install the required dependencies:
   
```bash
pip install -r requirements.txt
```

3. Configure the `sql_config.py` file with your MySQL database credentials.

4. Run the `main.py` script:

```bash
python main.py
```

## Configuration

Before running the script, make sure to configure the `sql_config.py` file with your MySQL database credentials:

```python
HOST = 'localhost'
USER = 'yourusername'
PASSWORD = 'yourpassword'
DATABASE = 'yourdatabase'
PORT = 3306  # Optional: Specify the port number if necessary
```

## Usage
Simply run the main.py script to generate a SQL backup file. The backup will be saved in the project directory with the name backup.sql.

```bash
python main.py
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
