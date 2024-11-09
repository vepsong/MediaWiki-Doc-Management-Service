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
    """rsync of a remote directory to the local VM."""
    try:
        command = [
            'rsync',
            '-avz',
            '--delete',
            '-e', f"ssh -i {PRIVATE_KEY_PATH} -o StrictHostKeyChecking=no",
            f"{REMOTE_USER}@{REMOTE_HOST}:{MEDIAWIKI_REMOTE_HOST_PATH}",
            MEDIAWIKI_DESTINATION_PATH
        ]
        
        # Executing the rsync command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Result output
        print("Synchronization result:")
        print(result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Error during synchronization:")
        print(e.stderr.decode('utf-8'))


def get_nginx_conf_file():
    """rsync of a remote directory to the local VM."""
    try:
        command = [
            'rsync',
            '-avz',
            '--delete',
            '-e', f"ssh -i {PRIVATE_KEY_PATH} -o StrictHostKeyChecking=no",
            f"{REMOTE_USER}@{REMOTE_HOST}:/etc/nginx/sites-available/{NGINX_CONF_FILE}",
            '/etc/nginx/sites-available/'
        ]
        
        # Executing the rsync command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Result output
        print("Synchronization result:")
        print(result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Error during synchronization:")
        print(e.stderr.decode('utf-8'))



def nginx_symlink_creation():
    """Create a symlink for the NGINX configuration file in /etc/nginx/sites-available/<nginx_conf_file_name>."""
    try:
        symlink_command = [
            'ln',
            '-s',
            f"/etc/nginx/sites-available/{NGINX_CONF_FILE}",
            f"/etc/nginx/sites-enabled/{NGINX_CONF_FILE}"
        ]
        
        # Symlink_command execution
        symlink_result  = subprocess.run(symlink_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Symlink creation results output
        print("Symlink created successfully:")
        print(symlink_result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("Error when creating symlink:")
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
        nginx_symlink_creation()
        print(f"nginx symlink conf file was successfully ended: {NOW}")


    except Exception as e:
        print(f"Error occurred: {e}")
