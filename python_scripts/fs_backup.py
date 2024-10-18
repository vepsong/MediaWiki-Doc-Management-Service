import os
import tarfile
from datetime import datetime

def backup_filesystem(source_dir, dest_dir):
    # Формируем имя файла резервной копии
    backup_filename = os.path.join(dest_dir, f"mediawiki_backup_{datetime.now().strftime('%Y%m%d')}.tar.gz")
    
    with tarfile.open(backup_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    
    print(f"Резервная копия файловой системы успешно создана: {backup_filename}")

if __name__ == "__main__":
    # Укажите директорию с файлами MediaWiki и директорию для резервного копирования
    source_directory = "/path/to/mediawiki/files"
    destination_directory = "/path/to/backup/directory"
    backup_filesystem(source_directory, destination_directory)
