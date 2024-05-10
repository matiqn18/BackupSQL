# BackupSQL

BackupSQL is a Python script designed for creating SQL backups of MySQL databases. This script establishes a connection with a MySQL database, retrieves table and column names, and exports the data into a SQL file for backup purposes. Additionally, it provides functionality to automatically restore data from a backup SQL file to a backup database.

## Features

- Connects to a MySQL database using specified credentials.
- Retrieves table names and column names from the connected database.
- Generates SQL queries to export table data.
- Saves the SQL backup to a file.
- Automatically save data to backup server

## Installation

To use BackupSQL, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/matiqn18/BackupSQL.git
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
#Main Server
HOST = 'localhost'
USER = 'yourusername'
PASSWORD = 'yourpassword'
DATABASE = 'yourdatabase'
PORT = 3306  # Optional: Specify the port number if necessary

#Backup Server
HOST_BACKUP = ''
USER_BACKUP = ''
PASSWORD_BACKUP = ''
DATABASE_BACKUP = ''
PORT_BACKUP =
```

## Usage
Simply run the main.py script to generate a SQL backup file and save it on the backup server. The backup will be saved in the project directory with the name backup.sql.

```bash
python main.py
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
