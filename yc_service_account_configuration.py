import json
import os
import subprocess

# Шаг 1. Открытие файла и загрузка данных
with open('YC_meta.json', 'r') as f:
    data = json.load(f)

# Извлечение нужных данных из JSON-файла
service_account_id = data.get('service_account_id')
cloud_id = data.get('cloud-id')
folder_id = data.get('folder-id')
profile_name = data.get('profile-name')


# Шаг 2. Создание SSH-ключа для аутентификации Terraform в Yandex Cloud
def create_ssh_key():
    print("Создание SSH-ключа для аутентификации...")
    command = [
        'yc', 'iam', 'key', 'create',
        '--service-account-id', service_account_id,
        '--folder-name', 'default',
        '--output', 'key.json'
    ]
    try:
        subprocess.run(command, check=True)
        print("SSH-ключ успешно создан.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании ключа: {e}")


# Шаг 3. Создание локального профиля yc
def create_yc_profile():
    print(f"Создание профиля {profile_name}...")
    command = ['yc', 'config', 'profile', 'create', profile_name]
    try:
        subprocess.run(command, check=True)
        print(f"Профиль {profile_name} успешно создан.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании профиля: {e}")


# Настройка конфигурации профиля
def configure_yc_profile():
    print("Настройка профиля...")
    try:
        # Установка ключа сервисного аккаунта
        subprocess.run(['yc', 'config', 'set', 'service-account-key', 'key.json'], check=True)

        # Установка cloud-id и folder-id
        subprocess.run(['yc', 'config', 'set', 'cloud-id', cloud_id], check=True)
        subprocess.run(['yc', 'config', 'set', 'folder-id', folder_id], check=True)

        print("Конфигурация профиля завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при настройке профиля: {e}")


# Шаг 4. Добавление переменных окружения в ~/.bashrc
def configure_bashrc():
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'a') as bashrc_file:
        bashrc_file.write('\n# Yandex Cloud environment variables\n')
        bashrc_file.write('export YC_TOKEN=$(yc iam create-token)\n')
        bashrc_file.write('export YC_CLOUD_ID=$(yc config get cloud-id)\n')
        bashrc_file.write('export YC_FOLDER_ID=$(yc config get folder-id)\n')

    print(f"Переменные окружения добавлены в {bashrc_path}.")
    print("Применение изменений...")

    # Используем bash для выполнения source
    subprocess.run(['bash', '-c', f"source {bashrc_path}"], check=True)


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
