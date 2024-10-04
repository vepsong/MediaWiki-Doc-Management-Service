import os
from utils import run_command, load_and_check_env_vars, copy_file

# Имена переменных, которые нужно загрузить
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1: Инициализация Terraform
def terraform_init(terraform_folder_path):
    """Инициализация Terraform."""

    # Выполняем команды перехода в директорию и инициализации Terraform
    command = ['terraform', 'init']
    run_command(command, cwd=terraform_folder_path, capture_output=False)


if __name__ == "__main__":
    user_home_path = os.path.expanduser('~/')
    provider_conf_file_name = ".terraformrc"
    provider_conf_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{provider_conf_file_name}'
    terraform_folder_path = f'{env_var_dic["TERRAFORM_ABSOLUTE_PATH"]}'

    # Копируем конфигурацию провайдера
    copy_file(provider_conf_file_path, user_home_path)
    # Инициализация Terraform
    terraform_init(terraform_folder_path)