from datetime import datetime, timedelta  
from pathlib import Path
import os
import re
from collections import OrderedDict
from pprint import pprint
import tempfile
import sys
from dotenv import load_dotenv
import subprocess

load_dotenv()

NOW = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT")

BACKUPS_PATH = Path(os.getenv("BACKUPS_DIR"))
PRIVATE_KEY_PATH = Path(os.getenv("PRIVATE_KEY_PATH"))
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_USER = os.getenv("REMOTE_USER")

REMOTE_PATH = '/var/www/mediawiki'
MEDIAWIKI_FOLDER_NAME = 'mediawiki'

ARCHIVE_SQL_DUMP_FILE_NAME = f'dump_sql_{DATABASE_NAME}_{NOW}.sql.gz'.replace('/', '_')
ARCHIVE_MEDIAWIKI_REMOTE_FOLDER_NAME = f'backup_{REMOTE_HOST}_{REMOTE_PATH}_{NOW}.tar.gz'.replace('/', '_')

BACKUP_SQL_PATTERN = re.compile(r"dump_sql_(.+)_(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})\.sql\.gz")
BACKUP_MEDIAWIKI_PATTERN = re.compile(r"backup_(.+)_(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})\.tar\.gz")


KEEP_LAST_N_BACKUPS = 10  # The number of backups that need to be retained


# Archiving to .tar.gz
def make_archive(dest_path, source_path):
    """Archiving to .tar.gz."""

    try:
        # Command for creating an archive
        tar_command = ['tar', '-czvf', dest_path, '-C', source_path, '.']
#         # Executing the archiving command
        tar_result = subprocess.run(tar_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Archiving completed successfully: {NOW}")
        print(tar_result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Error while creating the archive:")
        print(e.stderr.decode('utf-8'))

# Executing rsync of the remote directory to the local VM and archiving
def get_and_archive_remote_folder():
    """"rsync of the remote directory to the local VM and archiving."""
    try:
        command = [
            'rsync',
            '-avz',
            '--delete',
            '-e', f"ssh -i {PRIVATE_KEY_PATH} -o StrictHostKeyChecking=no",
            f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}",
            BACKUPS_PATH
        ]
        
        # Executing the rsync command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Outputting the results
        print("Synchronization result:")
        print(result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Error during synchronization:")
        print(e.stderr.decode('utf-8'))

    # Creating an archive after synchronization
    dest_path = f'{BACKUPS_PATH}/{ARCHIVE_MEDIAWIKI_REMOTE_FOLDER_NAME}'
    source_path = f'{BACKUPS_PATH}/{MEDIAWIKI_FOLDER_NAME}'
        
    make_archive(dest_path, source_path)




# Создание sql-dump'a БД"
def create_dump_postgres():
    """Creating an SQL dump of the database."""
    try:
        dest_path = f'{BACKUPS_PATH}/{ARCHIVE_SQL_DUMP_FILE_NAME}'

        command = (
            f"PGPASSWORD={DATABASE_PASSWORD} "
            f"pg_dump -U {DATABASE_USER} -p {DATABASE_PORT} -h localhost {DATABASE_NAME} "
            f"| gzip > {dest_path}"
        )

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command pg_dump was successfully executed")

    except Exception as e:
        print(f"Error in create_dump_postgres: {e.stderr.decode('utf-8')}")
        sys.exit(10)


def rotate_sql_backups(backups_by_db):
    """Rotation of SQL backups."""

    for db_name, backups in backups_by_db.items():
        # Sorting backups by creation time (according to the file name)
        backups.sort(key=lambda x: x[1], reverse=True)

        # If the number of backups is greater than the number to be retained:
        if len(backups) > KEEP_LAST_N_BACKUPS:
            print(f"Deleting old backups for {db_name}. Current count: {len(backups)}")
            for backup_to_delete in backups[KEEP_LAST_N_BACKUPS:]:
                print(f"Deleting old SQL backup: {backup_to_delete[0]}")
                backup_to_delete[0].unlink()  # File deleting
        else:
            print(f"No rotation needed for {db_name}. Current count: {len(backups)}")


def rotate_mediawiki_backups(backups_by_remote):
    """Rotation of MediaWiki backups."""
    for remote_host, backups in backups_by_remote.items():

        # Sorting backups by creation time (according to the file name)
        backups.sort(key=lambda x: x[1], reverse=True)

        # If the number of backups is greater than the number to be retained:
        if len(backups) > KEEP_LAST_N_BACKUPS:
            print(f"Deleting old backups for {remote_host}. Current count: {len(backups)}")
            for backup_to_delete in backups[KEEP_LAST_N_BACKUPS:]:
                print(f"Deleting old MediaWiki backup: {backup_to_delete[0]}")
                backup_to_delete[0].unlink()  # # File deleting
        else:
            print(f"No rotation needed for {remote_host}. Current count {len(backups)}")

def rotate_backups():
    """Rotating backup files and retaining only the last N copies for each database"""
    backups_by_db = {}  # For storing SQL backups by database
    backups_by_remote = {}  # For storing MediaWiki backups by remote servers

    # Iterating through files in the backup directory
    for backup_file in BACKUPS_PATH.iterdir():
        if backup_file.is_file():
            # Checking for SQL dumps
            sql_match = BACKUP_SQL_PATTERN.match(backup_file.name)
            if sql_match:
                db_name, timestamp = sql_match.groups()
                if db_name not in backups_by_db:
                    backups_by_db[db_name] = []
                backups_by_db[db_name].append((backup_file, timestamp))
            
            # Checking for MediaWiki dumps
            mediawiki_match = BACKUP_MEDIAWIKI_PATTERN.match(backup_file.name)
            if mediawiki_match:
                remote_host, timestamp = mediawiki_match.groups()
                if remote_host not in backups_by_remote:
                    backups_by_remote[remote_host] = []
                backups_by_remote[remote_host].append((backup_file, timestamp))

    try:           
        rotate_sql_backups(backups_by_db)
    except Exception as e:
        print(f"Error in rotate_sql_backups: {e}")
    try:           
        rotate_mediawiki_backups(backups_by_remote)
    except Exception as e:
        print(f"Error in rotate_mediawiki_backups: {e}")



if __name__ == "__main__":

    try:
        print(f"Backup script started: {NOW}")

        get_and_archive_remote_folder()
        create_dump_postgres()
        rotate_backups()

        print(f"Backup script was successfully ended: {NOW}")

    except Exception as e:
        print(f"Error occurred: {e}")
