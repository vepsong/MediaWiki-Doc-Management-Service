import json
import os
import subprocess
# Импортируем функцию получения имени репозитория
from utils import get_git_repo_name  


# Универсальная функция для выполнения команд с проверкой результата
def run_command(command):
    try:
        subprocess.run(command, check=True)
        print(f"Команда '{' '.join(command)}' успешно выполнена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")


# Функция для добавления переменной в bashrc
def add_env_variable_to_bashrc(variable_name, command):
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'a') as bashrc_file:
        bashrc_file.write(f'\n# Yandex Cloud environment variables\n')
        bashrc_file.write(f'export {variable_name}=$({command})\n')

    print(f"Переменная окружения {variable_name} добавлена в {bashrc_path}.")

# Шаг 1. Получение имени репозитория и построение пути
repo_name = get_git_repo_name()  # Получаем имя репозитория с помощью utils.py
if not repo_name:
    print("Не удалось получить имя репозитория.")
    exit(1)

# Строим путь к файлу yc_meta.json
json_file = os.path.expanduser(f"~/{repo_name}/credentials/yc_meta.json")

if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
else:
    print(f"Файл {json_file} не найден. Пожалуйста, убедитесь, что он существует.")
    exit(1)  # Завершаем выполнение программы

# Извлечение нужных данных из JSON-файла
service_account_id = data.get('service_account_id')
cloud_id = data.get('cloud-id')
folder_id = data.get('folder-id')
profile_name = data.get('profile-name')

# Определяем директорию, где находится yc_meta.json, для сохранения key.json
credentials_dir = os.path.dirname(json_file)  # Получаем директорию файла yc_meta.json
key_file_path = os.path.join(credentials_dir, 'key.json')  # Путь для key.json


# Шаг 2. Создание SSH-ключа для аутентификации Terraform в Yandex Cloud
def create_ssh_key():
    print("Создание SSH-ключа для аутентификации...")
    command = [
        'yc', 'iam', 'key', 'create',
        '--service-account-id', service_account_id,
        '--folder-name', 'default',
        '--output', key_file_path
    ]
    run_command(command)


# Шаг 3. Создание локального профиля yc
def create_yc_profile():
    print(f"Создание профиля {profile_name}...")
    command = ['yc', 'config', 'profile', 'create', profile_name]
    run_command(command)


# Настройка конфигурации профиля
def configure_yc_profile():
    print("Настройка профиля...")
    command_profile = ['yc', 'config', 'set', 'service-account-key', key_file_path]
    # Настройка ключа сервисного аккаунта
    run_command(command_profile)

    # Настройка cloud-id и folder-id
    command_cloud_id = ['yc', 'config', 'set', 'cloud-id', cloud_id]
    command_folder_id = ['yc', 'config', 'set', 'folder-id', folder_id]
    run_command(command_cloud_id)
    run_command(command_folder_id)

# Шаг 4. Добавление переменных окружения в ~/.bashrc
def configure_bashrc():
    add_env_variable_to_bashrc('YC_TOKEN', 'yc iam create-token')
    add_env_variable_to_bashrc('YC_CLOUD_ID', 'yc config get cloud-id')
    add_env_variable_to_bashrc('YC_FOLDER_ID', 'yc config get folder-id')

    # Используем bash для выполнения source
    command = ['bash', '-c', f"source ~/.bashrc"]
    run_command(command)


# Шаг 5. Проверка настроек после перезагрузки терминала
def check_env_variables():
    print("Для проверки переменных окружения перезапусти терминал и введи в командную строку следующие команды:")
    print("echo $YC_TOKEN")
    print("echo $YC_CLOUD_ID")
    print("echo $YC_FOLDER_ID")


# Выполнение всех шагов
if __name__ == "__main__":
    create_ssh_key()
    create_yc_profile()
    configure_yc_profile()
    configure_bashrc()
    check_env_variables()
