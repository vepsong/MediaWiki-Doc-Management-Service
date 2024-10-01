# Импортируем необходимые библиотеки
import os

# Путь к файлу с SSH-ключом
ssh_key_path = os.path.expanduser('~/.ssh/id_ed25519.pub')

# Чтение содержимого файла с SSH-ключом
try:
    with open(ssh_key_path, 'r') as key_file:
        ssh_key = key_file.read().strip()
except FileNotFoundError:
    print(f"Файл с ключом не найден: {ssh_key_path}")
    exit(1)

# Формирование содержимого для файла meta.txt
meta_content = f"""#cloud-config
users:
  - name: root
    groups: sudo
    shell: /bin/bash
    sudo: 'ALL=(ALL) NOPASSWD:ALL'
    ssh-authorized-keys:
      - {ssh_key}
"""

# Запись содержимого в файл meta.txt
with open('meta.txt', 'w') as meta_file:
    meta_file.write(meta_content)

print("Файл meta.txt успешно обновлен!")
