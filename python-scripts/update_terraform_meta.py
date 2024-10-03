# Импортируем необходимые библиотеки
import os
# Импортируем функцию получения названия репозитория
from utils import get_git_repo_name

# Получаем имя репозитория
repo_name = get_git_repo_name()

if not repo_name:
    print("Не удалось получить имя репозитория.")
    exit(1)

# Имя файла и путь к директории
file_name = "terraform_meta.txt"
file_path = os.path.expanduser(f"~/{repo_name}/credentials/{file_name}")


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
with open(file_path, 'w') as terraform_meta_file:
    terraform_meta_file.write(terraform_meta_content)

print(f"Файл {file_path} - успешно обновлен!")
