from datetime import datetime  
from pathlib import Path
import os
import re
from collections import OrderedDict
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

ARCHIVE_SQL_DUMP_FILE_NAME = f'dump_sql_{DATABASE_NAME}_{NOW}.sql.gz'.replace('/', '_')

BACKUP_SQL_PATTERN = re.compile(r"dump_sql_(.+)_(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})\.sql\.gz")

KEEP_LAST_N_BACKUPS = 10  # The number of backups that need to be retained

# # Archiving to .tar.gz
# def make_archive(dest_path, source_path):
#     """Archiving to .tar.gz."""

#     try:
#         # Command for creating an archive
#         tar_command = ['tar', '-czvf', dest_path, '-C', source_path, '.']
#         # Executing the archiving command
#         tar_result = subprocess.run(tar_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         print(f"Archiving completed successfully: {NOW}")
#         print(tar_result.stdout.decode('utf-8'))

#     except subprocess.CalledProcessError as e:
#         print("Error while creating the archive:")
#         print(e.stderr.decode('utf-8'))



# Step 1. Creating an SQL dump of the database
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

    try:           
        rotate_sql_backups(backups_by_db)
    except Exception as e:
        print(f"Error in rotate_sql_backups: {e}")




if __name__ == "__main__":

    try:
        print(f"Backup script started: {NOW}")

        create_dump_postgres()
        rotate_backups()

        print(f"Backup script was successfully ended: {NOW}")

    except Exception as e:
        print(f"Error occurred: {e}")
