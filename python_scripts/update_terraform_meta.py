# Импортируем необходимые библиотеки
import os
# Импортируем функцию загрузки и проверки необходимых переменных окружения, записи данных в txt-файл
from utils import load_and_check_env_vars, write_txt_to_file

# Имена переменных, которые нужно загрузить
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1. Проверка наличия публичного ssh-ключа
def check_ssh_public_key(ssh_public_key_path):
    """Чтение содержимого файла с публичным SSH-ключом."""
    try:
        with open(ssh_public_key_path, 'r') as key_file:
            ssh_key = key_file.read().strip()
            return ssh_key
    except FileNotFoundError:
        print(f"Файл с ключом не найден: {ssh_public_key_path}")
        exit(1)

# Шаг 2. Формирование содержимого для файла terraform_meta.txt
def create_terraform_meta_content(ssh_key):
    """Создает содержимое для файла terraform_meta.txt с переданным SSH-ключом."""
    try:
        # Спрашиваем у пользователя, хочет ли он оставить данные по умолчанию или изменить их
        choice = input("Нажмите enter, чтобы оставить данные по умолчанию, или введите 'change', чтобы изменить их: ").strip().lower()

        if choice == 'change':
            # Запрашиваем пользовательские значения
            print("Пустой ввод оставит значение поля по-умолчанию")
            name = input("Введите значение для 'name' (default: root): ") or "root"
            groups = input("Введите значение для 'groups' (default: sudo): ") or "sudo"
            shell = input("Введите значение для 'shell' (default: /bin/bash): ") or "/bin/bash"
            sudo = input("Введите значение для 'sudo' (default: 'ALL=(ALL) NOPASSWD:ALL'): ") or "ALL=(ALL) NOPASSWD:ALL"
        else:
            # Используем значения по умолчанию
            name = "root"
            groups = "sudo"
            shell = "/bin/bash"
            sudo = "ALL=(ALL) NOPASSWD:ALL"

        terraform_meta_content = f"""#cloud-config
users:
  - name: {name}
    groups: {groups}
    shell: {shell}
    sudo: '{sudo}'
    ssh-authorized-keys:
      - {ssh_key}
"""
        return terraform_meta_content
    except Exception as e:
        print(f"Произошла ошибка при формировании содержимого файла: {e}")
        exit(1)

if __name__ == "__main__":
    # Определение абсолютных путей к файлам и папкам
    file_name = "terraform_meta.txt"
    meta_file_in_credentials = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{file_name}'
    meta_file_in_terraform = f'{env_var_dic["TERRAFORM_ABSOLUTE_PATH"]}/{file_name}'
    ssh_public_key_path = os.path.expanduser('~/.ssh/id_ed25519.pub')

    ssh_key = check_ssh_public_key(ssh_public_key_path) # Проверка файла с публичным SSH-ключом
    terraform_meta_content = create_terraform_meta_content(ssh_key) # Формирование данных для записи в файл

    # Запись содержимого в файл terraform_meta.txt в две директории
    write_txt_to_file(terraform_meta_content, meta_file_in_credentials) # Для стандартизации хранения переменных авторизации
    write_txt_to_file(terraform_meta_content, meta_file_in_terraform) # Для использования Terraform'ом
