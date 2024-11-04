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

KEEP_LAST_N_BACKUPS = 10  # Количество бэкапов, которые нужно оставить


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


    # # Отладочная печать для проверки данных
    # print(f"backups_by_db (SQL): {backups_by_db}")
    # print(f"backups_by_remote (MediaWiki): {backups_by_remote}")

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
