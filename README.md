# BackupSQL

BackupSQL is a Python script designed for creating SQL backups of MySQL databases. This script establishes a connection with a MySQL database, retrieves table and column names, and exports the data into a SQL file for backup purposes. Additionally, it provides functionality to automatically restore data from a backup SQL file to a backup database.

## Features

- Connects to a MySQL database using specified credentials.
- Retrieves table names and column names from the connected database.
- Generates SQL queries to export table data.
- Saves the SQL backup to a file.
- Automatically sends data to the backup server if BACKUP_LIVE variable is set to true.
- Supports execution using environment variables for configuration.

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

Before running the script, make sure to configure the `sql_config.py` file with your MySQL database credentials. Alternatively you can use environment variables to configure the description of the names is below, the configuration method corresponds to the one in the `sql_config.py` file

```python
# Main Server
HOST = 'localhost'
USER = 'yourusername'
PASSWORD = 'yourpassword'
DATABASE = 'yourdatabase'
PORT =   # Optional: Specify the port number if necessary

# Backup Live Setting
BACKUP_LIVE = True  # Set to True to enable sending data to backup server

# Backup Server
HOST_BACKUP = 'backupserver'
USER_BACKUP = 'backupusername'
PASSWORD_BACKUP = 'backuppassword'
DATABASE_BACKUP = 'backupdatabase'
PORT_BACKUP =   # Optional: Specify the port number if necessary
```

## Usage
Simply run the main.py script to generate a SQL backup file and optionally send it to the backup server. The backup will be saved in the project directory with the name backup.sql. 

```bash
python main.py
```

## Usage with GitHub Actions

If you plan to use this script with GitHub Actions, we recommend creating appropriate secrets in your repository. These secrets will store sensitive information such as database passwords. To do this, follow these steps:

1. Go to the settings of your repository on GitHub.
2. Select the "Secrets" section from the menu on the left.
3. Click the "New repository secret" button.
4. Create secrets with the following names:
   - `MYSQL_HOST`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`
   - `MYSQL_PORT` (optional)
   - `BACKUP_LIVE`
   - `HOST_BACKUP`
   - `USER_BACKUP`
   - `PASSWORD_BACKUP`
   - `DATABASE_BACKUP`
   - `PORT_BACKUP` (optional)

You can then use these secrets in your GitHub Actions scripts, ensuring the secure storage of sensitive data.

## Usage as a Submodule

If you want to use this repository as a submodule in another project, execute the following command:

```bash
git submodule add https://github.com/matiqn18/BackupSQL.git BackupSQL
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
