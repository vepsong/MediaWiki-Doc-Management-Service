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



# под удаление
SQL_DUMP_FILE_NAME = f'dump_{DATABASE_NAME}_{NOW}.sql'
ARCHIVE_FILE_NAME = f'archive_sql_dump_{DATABASE_NAME}_and_mediawiki_folder_{NOW}.tar.gz'

REMOTE_PATH = '/var/www/mediawiki'
MEDIAWIKI_FOLDER_NAME = 'mediawiki'

ARCHIVE_SQL_DUMP_FILE_NAME = f'dump_{DATABASE_NAME}_{NOW}.sql'
ARCHIVE_MEDIAWIKI_REMOTE_FOLDER_NAME = f'backup_{REMOTE_HOST}_{REMOTE_PATH}_{NOW}.tar.gz'.replace('/', '_')

BACKUP_PATTERN = re.compile(r"archive_sql_dump_(.+)_and_mediawiki_folder_(\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.tar\.gz")
KEEP_LAST_N_BACKUPS = 10  # Количество бэкапов, которые нужно ост


def get_remote_folder():
    try:
        command = [
            'rsync',
            '-avz',
            '--delete',
            '-e', f"ssh -i {PRIVATE_KEY_PATH}",
            f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}",
            BACKUPS_PATH
        ]
        
        # Выполнение команды rsync
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Вывод результатов
        print("Результат синхронизации:")
        print(result.stdout.decode('utf-8'))

        # Создание архива после синхронизации
        archive_path = f'{BACKUPS_PATH}/{ARCHIVE_MEDIAWIKI_REMOTE_FOLDER_NAME}'
        mediawiki_folder_path = f'{BACKUPS_PATH}/{MEDIAWIKI_FOLDER_NAME}'

        # Команда для создания архива
        tar_command = ['tar', '-czvf', archive_path, '-C', mediawiki_folder_path, '.']
        # Выполнение команды архивации
        tar_result = subprocess.run(tar_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Архивация завершена:")
        print(tar_result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Ошибка при синхронизации:")
        print(e.stderr.decode('utf-8'))




def create_backup_combine_archive(now):
    try:
        print("create_backup_file started")
        combine_archive_filename = f'{BACKUPS_PATH}/{ARCHIVE_FILE_NAME}'
        

        with tempfile.TemporaryDirectory() as tmpdirname:
            sql_dump_filepath = f'{Path(tmpdirname)}/{SQL_DUMP_FILE_NAME}'

            create_dump_postgres(sql_dump_filepath)

            archive_tar_command = (
            f'tar -czf {combine_archive_filename} '
            f'-C {sql_dump_filepath} -C {BACKUPS_PATH}/{MEDIAWIKI_FOLDER_NAME}'
            )

            result = subprocess.run(archive_tar_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result != 0:
                raise Exception(f"tar failed with code {result}, command = {archive_tar_command}")

    except Exception as e:
        print(f"Error in create_backup_file: {e}")
        sys.exit(1)


# Создание sql-dump'a БД"
def create_dump_postgres(sql_dump_filepath):
    """Создание sql-dump'a БД"""
    try:
        pg_dump_command = (
            f'PGPASSWORD={DATABASE_PASSWORD} '
            f'pg_dump -U {DATABASE_USER} {DATABASE_NAME} -p {DATABASE_PORT} '
            f'-h localhost > {sql_dump_filepath}'
        )

        result = subprocess.run(pg_dump_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result != 0:
            raise Exception(f"pg_dump failed with code {result}, command = {pg_dump_command}")
    except Exception as e:
        print(f"Error in create_dump_postgres: {e}")
        sys.exit(10)



def rotate_backups():
    """
    Функция для ротации файлов резервных копий, оставляет только последние N копий для каждой базы данных.
    """
    backups_by_db = {}

    # Перебираем файлы в директории бэкапов
    for backup_file in BACKUPS_PATH.iterdir():
        if backup_file.is_file():
            match = BACKUP_PATTERN.match(backup_file.name)
            if match:
                db_name, timestamp = match.groups()
                if db_name not in backups_by_db:
                    backups_by_db[db_name] = []
                backups_by_db[db_name].append((backup_file, timestamp))

    # Ротация бэкапов
    for db_name, backups in backups_by_db.items():
        # Сортируем бэкапы по времени создания (в имени файла)
        backups.sort(key=lambda x: x[1], reverse=True)

        # Если количество бэкапов больше, чем нужно сохранить
        if len(backups) > KEEP_LAST_N_BACKUPS:
            for backup_to_delete in backups[KEEP_LAST_N_BACKUPS:]:
                print(f"Удаляю старый бэкап: {backup_to_delete[0]}")
                backup_to_delete[0].unlink()  # Удаление файла



if __name__ == "__main__":

    try:
        print(f"Backup script started: {NOW}")

        get_remote_folder()
        create_backup_combine_archive(NOW)
        rotate_backups(NOW)

        print(f"Backup prod data script was successfully ended. timestamp: {NOW}")
    except Exception as e:
        print(f"Error occurred: {e}")



