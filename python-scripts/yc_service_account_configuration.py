from utils import run_command, add_env_variable_to_bashrc, load_and_check_env_vars, load_json_data

# Имена переменных, которые нужно загрузить
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)

# Шаг 1. Создание файла с данными аутентификации сервисного аккаунта Yandex Cloud (для работы с Terraform)
def create_service_yc_account_ssh_key(yc_meta_file_data, yc_meta_key_file_path):
    """Создание файла с данными аутентификации сервисного аккаунта Yandex Cloud (для работы с Terraform)."""
    
    service_account_id = yc_meta_file_data['service_account_id']

    command = [
        'yc', 'iam', 'key', 'create',
        '--service-account-id', service_account_id,
        '--folder-name', 'default',
        '--output', yc_meta_key_file_path
    ]
    run_command(command)


# Шаг 2. Создание локального профиля yc
def create_yc_profile(yc_meta_file_data):
    """Создание локального профиля yc."""

    profile_name = yc_meta_file_data['profile-name']

    print(f"Создание профиля {profile_name}...")
    command = ['yc', 'config', 'profile', 'create', profile_name]
    run_command(command)


# Шаг 3. Настройка локального профиля yc
def configure_yc_profile(yc_meta_file_data, yc_meta_key_file_path):
    """Настройка локального профиля yc."""
    
    profile_name = yc_meta_file_data['profile-name']
    cloud_id = yc_meta_file_data['cloud-id']
    folder_id = yc_meta_file_data['folder-id']

    print(f"Настройка профиля {profile_name}...")

    # Настройка ssh-ключа сервисного аккаунта
    command_profile = ['yc', 'config', 'set', 'service-account-key', yc_meta_key_file_path]
    run_command(command_profile)

    # Настройка cloud-id и folder-id
    command_cloud_id = ['yc', 'config', 'set', 'cloud-id', cloud_id]
    command_folder_id = ['yc', 'config', 'set', 'folder-id', folder_id]
    run_command(command_cloud_id)
    run_command(command_folder_id)

# Шаг 4. Добавление переменных окружения в ~/.bashrc
def configure_bashrc():
    add_env_variable_to_bashrc('YC_TOKEN', '$(yc iam create-token)')
    add_env_variable_to_bashrc('YC_CLOUD_ID', '$(yc config get cloud-id)')
    add_env_variable_to_bashrc('YC_FOLDER_ID', '$(yc config get folder-id)')

    # Используем bash для выполнения source
    command = ['bash', '-c', f"source ~/.bashrc"]
    run_command(command)

    print("Для проверки переменных окружения перезапустить терминал и ввести: echo $<переменная окружения>")


# Выполнение всех шагов
if __name__ == "__main__":

    # Название файла с данными
    yc_meta_file = "yc_meta.json"

    # Название файла вывода с данными
    yc_meta_key_file = "key.json"

    # Абсолютный путь к файлам данных
    yc_meta_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{yc_meta_file}'
    yc_meta_key_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{yc_meta_key_file}'

    # Получение данных из "yc_meta.json"
    yc_meta_file_data = load_json_data(yc_meta_file_path)
    # Создание файла с данными аутентификации сервисного аккаунта Yandex Cloud (для работы с Terraform)
    create_service_yc_account_ssh_key(yc_meta_file_data, yc_meta_key_file_path)
    # Создание локального профиля yc
    create_yc_profile(yc_meta_file_data)
    # Настройка локального профиля yc
    configure_yc_profile(yc_meta_file_data, yc_meta_key_file_path)
    # Добавление переменных окружения в ~/.bashrc
    configure_bashrc()
