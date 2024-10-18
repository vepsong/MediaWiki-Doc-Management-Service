import os
import subprocess
from datetime import datetime

def backup_database(db_name, db_user, dest_dir):
    # Формируем имя файла резервной копии
    backup_filename = os.path.join(dest_dir, f"db_backup_{datetime.now().strftime('%Y%m%d')}.sql")

    # Выполняем команду pg_dump
    command = f"pg_dump -U {db_user} -F c -b -v -f {backup_filename} {db_name}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Резервная копия базы данных успешно создана: {backup_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии базы данных: {e}")

if __name__ == "__main__":
    # Укажите имя базы данных, пользователя и директорию для резервного копирования
    database_name = "my_wiki"
    database_user = "syncuser"
    destination_directory = "/opt/db_mount_dump/pgdump"
    backup_database(database_name, database_user, destination_directory)
