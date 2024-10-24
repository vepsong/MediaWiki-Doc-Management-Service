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


# BACKUP_SQL_PATTERN = re.compile(r"dump_sql_(.+)_(\d{2}_\d{2}_\d{4}_\d{2}_\d{2}_\d{2})\.sql\.gz")
# BACKUP_MEDIAWIKI_PATTERN = re.compile(r"backup_(.+)_(\d{2}_\d{2}_\d{4}_\d{2}_\d{2}_\d{2})\.tar\.gz")

KEEP_LAST_N_BACKUPS = 10  # Количество бэкапов, которые нужно ост


def make_archive(dest_path, source_path):
    """Архивирование .tar.gz."""

    try:
        # Команда для создания архива
        tar_command = ['tar', '-czvf', dest_path, '-C', source_path, '.']
        # Выполнение команды архивации
        tar_result = subprocess.run(tar_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Архивация успешно завершена: {NOW}")
        print(tar_result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Ошибка при создании архива:")
        print(e.stderr.decode('utf-8'))


def get_and_archive_remote_folder():
    """rsync удаленной директории на локальную ВМ и архивация."""
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

    except subprocess.CalledProcessError as e:
        print("Ошибка при синхронизации:")
        print(e.stderr.decode('utf-8'))

    # Создание архива после синхронизации
    dest_path = f'{BACKUPS_PATH}/{ARCHIVE_MEDIAWIKI_REMOTE_FOLDER_NAME}'
    source_path = f'{BACKUPS_PATH}/{MEDIAWIKI_FOLDER_NAME}'
        
    make_archive(dest_path, source_path)




# Создание sql-dump'a БД"
def create_dump_postgres():
    """Создание sql-dump'a БД"""
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
    """Ротация SQL бэкапов."""

    for db_name, backups in backups_by_db.items():
        # Сортируем бэкапы по времени создания (в имени файла)
        backups.sort(key=lambda x: x[1], reverse=True)

        # Если количество бэкапов больше, чем нужно сохранить
        if len(backups) > KEEP_LAST_N_BACKUPS:
            print(f"Удаляем старые бэкапы для {db_name}. Текущее количество: {len(backups)}")
            for backup_to_delete in backups[KEEP_LAST_N_BACKUPS:]:
                print(f"Удаляю старый SQL бэкап: {backup_to_delete[0]}")
                backup_to_delete[0].unlink()  # Удаление файла
        else:
            print(f"Нет необходимости в ротации для {db_name}. Текущее количество: {len(backups)}")


def rotate_mediawiki_backups(backups_by_remote):
    """Ротация MediaWiki бэкапов."""
    for remote_host, backups in backups_by_remote.items():

        # Сортируем бэкапы по времени создания (в имени файла)
        backups.sort(key=lambda x: x[1], reverse=True)

        # Если количество бэкапов больше, чем нужно сохранить
        if len(backups) > KEEP_LAST_N_BACKUPS:
            print(f"Удаляем старые бэкапы для {remote_host}. Текущее количество: {len(backups)}")
            for backup_to_delete in backups[KEEP_LAST_N_BACKUPS:]:
                print(f"Удаляю старый MediaWiki бэкап: {backup_to_delete[0]}")
                backup_to_delete[0].unlink()  # Удаление файла
        else:
            print(f"Нет необходимости в ротации для {remote_host}. Текущее количество: {len(backups)}")

def rotate_backups():
    """
    Функция для ротации файлов резервных копий, оставляет только последние N копий для каждой базы данных.
    """
    backups_by_db = {}  # Для хранения SQL бэкапов по БД
    backups_by_remote = {}  # Для хранения MediaWiki бэкапов по удаленным серверам

    # Перебираем файлы в директории бэкапов
    for backup_file in BACKUPS_PATH.iterdir():
        if backup_file.is_file():
            # Проверка на SQL дампы
            sql_match = BACKUP_SQL_PATTERN.match(backup_file.name)
            if sql_match:
                db_name, timestamp = sql_match.groups()
                if db_name not in backups_by_db:
                    backups_by_db[db_name] = []
                backups_by_db[db_name].append((backup_file, timestamp))
            
            # Проверка на MediaWiki бэкапы
            mediawiki_match = BACKUP_MEDIAWIKI_PATTERN.match(backup_file.name)
            if mediawiki_match:
                remote_host, timestamp = mediawiki_match.groups()
                if remote_host not in backups_by_remote:
                    backups_by_remote[remote_host] = []
                backups_by_remote[remote_host].append((backup_file, timestamp))

    # # Отладочная печать для проверки данных
    # print(f"backups_by_db (SQL): {backups_by_db}")
    # print(f"backups_by_remote (MediaWiki): {backups_by_remote}")

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



