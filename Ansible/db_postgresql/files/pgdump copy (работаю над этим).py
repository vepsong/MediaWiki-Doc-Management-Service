from datetime import datetime, timedelta  
from pathlib import Path
import os
import re
from collections import OrderedDict
from pprint import pprint
import tempfile
import sys
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = Path(os.getenv("DATABASE_NAME"))
BACKUPS_PATH = Path(os.getenv("BACKUPS_DIR"))
BACKUP_FILENAME_TEMPLATE = "{database_name}_dump_{now}.tar.gz"
SQLDUMP_FILENAME_TEMPLATE = "{database_name}_dump_{now}.sql"
PG_DUMP_COMMAND_TEMPLATE = "PGPASSWORD={password} pg_dump -U {user} {database} -p {port} -h localhost > {filename}"
TAR_COMMAND_TEMPLATE = "tar -czf {archive_filename} -C {dump_dirname} {dump_filename} -C {media_dirpath} {media_dirname}"
FILENAME_DATETIME_FORMAT = "%d-%m-%Y_%H-%M-%S"
BACKUPS_TIMETABLE = [0, 1, 2, 3, 7, 30, 180, 360]
DUMP_MINIMAL_FILESIZE = int(os.getenv("DUMP_MINIMAL_FILESIZE_MB")) * 1024 * 1024



def create_backup_file(now):
    try:
        print("create_backup_file started")
        archive_filename = BACKUPS_PATH / BACKUP_FILENAME_TEMPLATE.format(database_name=DATABASE_NAME, now=now)

        with tempfile.TemporaryDirectory() as tmpdirname:
            dump_filename = SQLDUMP_FILENAME_TEMPLATE.format(database_name=DATABASE_NAME, now=now)
            dump_filepath = Path(tmpdirname) / dump_filename
            create_dump_postgres(now, dump_filepath)
            
            tar_command = TAR_COMMAND_TEMPLATE.format(
                archive_filename=archive_filename,
                dump_dirname=tmpdirname,
                dump_filename=dump_filename,
                media_dirpath=os.getenv("MEDIA_DIRPATH"),
                media_dirname=os.getenv("MEDIA_DIRNAME"),
            )
            print(f"tar_command = {tar_command}")
            
            result = os.system(tar_command)
            if result != 0:
                raise Exception(f"tar failed with code {result}, command = {tar_command}")
            
            file_size = os.path.getsize(archive_filename)
            if file_size < DUMP_MINIMAL_FILESIZE:
                print(f"Database dump filesize is too small {file_size} bytes. Expected to be more than {DUMP_MINIMAL_FILESIZE} bytes")
    
    except Exception as e:
        print(f"Error in create_backup_file: {e}")
        sys.exit(1)

def create_dump_postgres(now, dump_filename):
    try:
        command = PG_DUMP_COMMAND_TEMPLATE.format(
            password=os.getenv("DATABASE_PASSWORD"),
            user=os.getenv("DATABASE_USER"),
            database=os.getenv("DATABASE_NAME"),
            port=os.getenv("DATABASE_PORT"),
            filename=dump_filename,
        )
        result = os.system(command)
        if result != 0:
            raise Exception(f"pg_dump failed with code {result}, command = {command}")
    except Exception as e:
        print(f"Error in create_dump_postgres: {e}")
        sys.exit(10)

def rotate_backups(now):
    try:
        def add_backup(intervals, backup):
            for interval in intervals:
                if interval["start"] <= backup["timestamp"] and backup["timestamp"] < interval["end"]:
                    interval["backups"].append(backup)
                    return
            print(f"found a file that does not belong to any interval: {backup}")

        def clear_extra_backups(intervals):
            for interval in intervals:
                backups = sorted(interval["backups"], key=lambda a: a["timestamp"], reverse=True)
                for i in range(len(backups) - 1):
                    filename = backups[i]["filename"]
                    print(f"deleting extra backup: {filename}")
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
                print(f"unexpected directory: {filename}")
            else:
                found = re.search("server_prod_(.+)\.tar\.gz", filename.name)
                if found is None:
                    print(f"found file without date in name: {filename}")
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

if __name__ == "__main__":

    now = datetime.now()
    now_str = now.strftime(FILENAME_DATETIME_FORMAT)
    try:
        print(f"Backup script started: {now_str}")
        create_backup_file(now_str)
        rotate_backups(now)
        print(f"Backup prod data script was successfully ended. timestamp: {now_str}")
    except Exception as e:
        print(f"Error occurred: {e}")
