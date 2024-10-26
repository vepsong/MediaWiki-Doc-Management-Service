from datetime import datetime  
from pathlib import Path
import os
import re
from dotenv import load_dotenv
import subprocess

load_dotenv()

NOW = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

PRIVATE_KEY_PATH = Path(os.getenv("PRIVATE_KEY_PATH"))
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_USER = os.getenv("REMOTE_USER")

MEDIAWIKI_REMOTE_HOST_PATH = os.getenv("MEDIAWIKI_REMOTE_HOST_PATH")
MEDIAWIKI_REMOTE_LOCAL_SETTINGS_FILE = os.getenv("MEDIAWIKI_LOCAL_SETTINGS_FILE")

MEDIAWIKI_DESTINATION_PATH = os.getenv("MEDIAWIKI_DESTINATION_PATH")

NGINX_CONF_FILE = os.getenv("NGINX_CONF_FILE")


def get_rsync_mediawiki_folder():
    """rsync удаленной директории на локальную ВМ."""
    try:
        command = [
            'rsync',
            '-avz',
            '--delete',
            '-e', f"ssh -i {PRIVATE_KEY_PATH} -o StrictHostKeyChecking=no",
            f"{REMOTE_USER}@{REMOTE_HOST}:{MEDIAWIKI_REMOTE_HOST_PATH}",
            MEDIAWIKI_DESTINATION_PATH
        ]
        
        # Выполнение команды rsync
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Вывод результатов
        print("Результат синхронизации:")
        print(result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Ошибка при синхронизации:")
        print(e.stderr.decode('utf-8'))


def get_nginx_conf_file():
    """rsync удаленной директории на локальную ВМ."""
    try:
        command = [
            'rsync',
            '-avz',
            '--delete',
            '-e', f"ssh -i {PRIVATE_KEY_PATH} -o StrictHostKeyChecking=no",
            f"{REMOTE_USER}@{REMOTE_HOST}:/etc/nginx/sites-available/{NGINX_CONF_FILE}",
            '/etc/nginx/sites-available/'
        ]
        
        # Выполнение команды rsync
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Вывод результатов
        print("Результат синхронизации:")
        print(result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Ошибка при синхронизации:")
        print(e.stderr.decode('utf-8'))



def nginx_synlink_creation():
    """Создание символической ссылки на конфиг nginx в /etc/nginx/sites-available/."""
    try:
        symlink_command = [
            'ln',
            '-s',
            f"/etc/nginx/sites-available/{NGINX_CONF_FILE}",
            f"/etc/nginx/sites-enabled/{NGINX_CONF_FILE}"
        ]
        
        # Выполнение symlink_command
        symlink_result  = subprocess.run(symlink_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Вывод результатов создания symlink
        print("Символическая ссылка создана успешно:")
        print(symlink_result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Ошибка при создании symlink:")
        print(e.stderr.decode('utf-8'))



if __name__ == "__main__":

    try:
        print(f"rsync mediawiki folder script started: {NOW}")
        get_rsync_mediawiki_folder()
        print(f"rsync mediawiki folder script was successfully ended: {NOW}")

        print(f"rsync nginx conf file started: {NOW}")
        get_nginx_conf_file()
        print(f"rsync nginx conf file was successfully ended: {NOW}")

        print(f"nginx symlink conf file started: {NOW}")
        nginx_synlink_creation()
        print(f"nginx symlink conf file was successfully ended: {NOW}")


    except Exception as e:
        print(f"Error occurred: {e}")
