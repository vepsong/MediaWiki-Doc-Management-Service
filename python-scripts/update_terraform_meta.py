# Импортируем необходимые библиотеки
import os
# Импортируем функцию получения названия репозитория и функцию получения названия папки Terraform
from utils import get_git_repo_name, find_directory_by_pattern


# Получаем имя репозитория
repo_name = get_git_repo_name()

if not repo_name:
    print("Не удалось получить имя репозитория.")
    exit(1)

# _, terraform_folder_name = find_terraform_directory(repo_name)
_, terraform_folder_name = find_directory_by_pattern(repo_name, file_extension=".tf")

# Имя файла и путь к директории
file_name = "terraform_meta.txt"
file_path_credentials = os.path.expanduser(f"~/{repo_name}/credentials/{file_name}")
file_path_terraform = os.path.expanduser(f"~/{repo_name}/{terraform_folder_name}/{file_name}")


# Путь к файлу с SSH-ключом
ssh_key_path = os.path.expanduser('~/.ssh/id_ed25519.pub')

# Чтение содержимого файла с SSH-ключом
try:
    with open(ssh_key_path, 'r') as key_file:
        ssh_key = key_file.read().strip()
except FileNotFoundError:
    print(f"Файл с ключом не найден: {ssh_key_path}")
    exit(1)

# Формирование содержимого для файла terraform_meta.txt
terraform_meta_content = f"""#cloud-config
users:
  - name: root
    groups: sudo
    shell: /bin/bash
    sudo: 'ALL=(ALL) NOPASSWD:ALL'
    ssh-authorized-keys:
      - {ssh_key}
"""

# Запись содержимого в файл terraform_meta.txt
# Файлы сохраняются в 2-х директориях:
# В ~/<repo_name>/credentials/ — для стандартизации хранения переменных авторизации
# В В ~/<repo_name>/<terraform_folder>/ — для использования Terraform'ом

try:
    with open(file_path_credentials, 'w') as meta_in_credentials, open(file_path_terraform, 'w') as meta_in_terraform:
        meta_in_credentials.write(terraform_meta_content)
        meta_in_terraform.write(terraform_meta_content)

    print(f"Файлы {file_path_credentials} и {file_path_terraform} - успешно обновлены!")
except Exception as e:
    print(f"Произошла ошибка при записи файлов: {e}")
