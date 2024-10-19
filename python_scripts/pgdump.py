from datetime import datetime, timedelta  
from pathlib import Path
import os
import re
from pprint import pprint
import tempfile
import sys
from dotenv import load_dotenv

load_dotenv()

BACKUPS_PATH = Path(os.getenv("BACKUPS_DIR"))

BACKUP_FILENAME_TEMPLATE = "server_prod_{now}.tar.gz"
SQLDUMP_FILENAME_TEMPLATE = "server_prod_{now}.sql"
PG_DUMP_COMMAND_TEMPLATE = "PGPASSWORD={password} pg_dump -U {user} {database} -p {port} -h localhost > {filename}"
TAR_COMMAND_TEMPLATE = "tar -czf {archive_filename} -C {dump_dirname} {dump_filename} -C {media_dirpath} {media_dirname}"
FILENAME_DATETIME_FORMAT = "%Y_%m_%d_%H_%M_%S"
BACKUPS_TIMETABLE = [0, 1, 2, 3, 7, 30, 180, 360]
# DUMP_MINIMAL_FILESIZE = int(os.getenv("DUMP_MINIMAL_FILESIZE_MB")) * 1024 * 1024


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
                    interval["backups"].append(backup)
                    return
            print(f"Found a file that does not belong to any interval: {backup}")

        def clear_extra_backups(intervals):
            for interval in intervals: 
                backups = sorted(interval["backups"], key=lambda a: a["timestamp"], reverse=True)
                for i in range(len(backups) - 1):
                    filename = backups[i]["filename"] 
                    print(f"Deleting extra backup: {filename}")
                    os.remove(filename)
                    backups[i]["status"] = "deleted" 

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


if __name__ == "__main__":
    try:
        now = datetime.now()
        now_str = now.strftime(FILENAME_DATETIME_FORMAT)
        print(f"Backup script started: {now_str}")

        # Создание дампа базы данных
        dump_filepath = create_dump_postgres(now_str)
        
        rotate_backups(now)
        print(f"Backup prod data script was successfully ended. timestamp: {now_str}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)