from datetime import datetime, timedelta  
from pathlib import Path
import os
import re
import sys
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

BACKUPS_PATH = Path(os.getenv("BACKUPS_DIR"))

BACKUP_FILENAME_TEMPLATE = "server_prod_{now}.tar.gz"
SQLDUMP_FILENAME_TEMPLATE = "server_prod_{now}.sql"
PG_DUMP_COMMAND_TEMPLATE = "PGPASSWORD={password} pg_dump -U {user} {database} -p {port} -h localhost > {filename}"
TAR_COMMAND_TEMPLATE = "tar -czf {archive_filename} -C {dump_dirname} {dump_filename}"
FILENAME_DATETIME_FORMAT = "%Y_%m_%d_%H_%M_%S"


# Переменные для настройки
MIN_BACKUP_INTERVAL = timedelta(minutes=240)  # Минимальный интервал между резервными копиями
MAX_BACKUPS = 3  # Максимальное количество резервных копий для хранения

# В каждом интервале всегда находится только {MAX_BACKUPS} бэкапов попадающих в интервал, 
# другой бэкап либо сдвигается в следующий интервал, либо удаляется.
# Бэкап попадающий в интервал между:
# 0 и 1, - бэкап за 1 день,
# 1 и 2, - за 2 день,
# 2 и 3, - за 3 день,
# 3 и 7, за 1 неделю,
# 7 и 30, за 1 месяц, и т.д.

BACKUPS_TIMETABLE = [0, 1, 2, 3, 7, 30, 180, 360]

def create_dump_postgres(now):     
    try:
        dump_filename = SQLDUMP_FILENAME_TEMPLATE.format(now=now)
        dump_filepath = BACKUPS_PATH / dump_filename  # Путь к файлу дампа

        command = PG_DUMP_COMMAND_TEMPLATE.format(
            password=os.getenv("DATABASE_PASSWORD"),
            user=os.getenv("DATABASE_USER"),
            database=os.getenv("DATABASE_NAME"),
            port=os.getenv("DATABASE_PORT"),
            filename=dump_filepath,
        )
        
        result = os.system(command)
        if result != 0:
            print(f"pg_dump failed with code {result}, command = {command}")
            sys.exit(10)

        return dump_filepath  # Возвращаем путь к созданному файлу дампа
    except Exception as e:
        print(f"Error in create_dump_postgres: {e}")
        sys.exit(1)

def rotate_backups(now):
    try:
        def add_backup(intervals, backup):
            for interval in intervals:
                if interval["start"] <= backup["timestamp"] < interval["end"]:
                    # Проверка времени между резервными копиями
                    if not interval["backups"] or (backup["timestamp"] - interval["backups"][-1]["timestamp"]) >= MIN_BACKUP_INTERVAL:
                        interval["backups"].append(backup)
                    else:
                        print(f"Skipping backup {backup['filename']} due to minimum interval restriction.")
                    return
            print(f"Found a file that does not belong to any interval: {backup}")

        def clear_extra_backups(intervals):
            for interval in intervals: 
                backups = sorted(interval["backups"], key=lambda a: a["timestamp"], reverse=True)
                # Удалить лишние резервные копии, оставив только MAX_BACKUPS
                if len(backups) > MAX_BACKUPS:
                    for backup in backups[MAX_BACKUPS:]:
                        filename = backup["filename"] 
                        print(f"Deleting extra backup: {filename}")
                        os.remove(filename)
                        backup["status"] = "deleted" 

        print("rotate_backups started") 
        intervals = []
        for i in range(len(BACKUPS_TIMETABLE) - 1):
            end = BACKUPS_TIMETABLE[i]
            start = BACKUPS_TIMETABLE[i + 1]
            intervals.append({
                "start": now - timedelta(days=start), 
                "end": now - timedelta(days=end),
                "backups": [],
                "days_end": BACKUPS_TIMETABLE[i],
                "days_start": BACKUPS_TIMETABLE[i + 1],
            })

        for filename in BACKUPS_PATH.iterdir():
            if filename.is_dir():
                print(f"Unexpected directory: {filename}")
            else:
                found = re.search("server_prod_(.+)\\.tar\\.gz", filename.name)
                if found is None:
                    print(f"Found file without date in name: {filename}")
                else: 
                    timestamp = found.group(1)    
                    timestamp = datetime.strptime(timestamp, FILENAME_DATETIME_FORMAT)
                    add_backup(intervals, {
                        "timestamp": timestamp,
                        "filename": filename,
                        "status": "exists",
                    }) 

        clear_extra_backups(intervals)       
        pprint(intervals)
    except Exception as e:
        print(f"Error in rotate_backups: {e}")
        sys.exit(1)

def archive_dump(dump_filepath):
    try:
        now = datetime.now().strftime(FILENAME_DATETIME_FORMAT)
        archive_filename = BACKUP_FILENAME_TEMPLATE.format(now=now)
        archive_filepath = BACKUPS_PATH / archive_filename  # Путь к архиву

        command = TAR_COMMAND_TEMPLATE.format(
            archive_filename=archive_filepath,
            dump_dirname=dump_filepath.parent,  # Директория, где находится дамп
            dump_filename=dump_filepath.name,     # Имя файла дампа
        )

        result = os.system(command)
        if result != 0:
            print(f"tar command failed with code {result}, command = {command}")
            sys.exit(10)

        return archive_filepath  # Возвращаем путь к созданному архиву
    except Exception as e:
        print(f"Error in archive_dump: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        now = datetime.now()
        now_str = now.strftime(FILENAME_DATETIME_FORMAT)
        print(f"Backup script started: {now_str}")

        # Создание дампа базы данных
        dump_filepath = create_dump_postgres(now_str)

        # Архивирование дампа
        archive_filepath = archive_dump(dump_filepath)

        # Управление резервными копиями
        rotate_backups(now)
        print(f"Backup prod data script was successfully ended. timestamp: {now_str}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
