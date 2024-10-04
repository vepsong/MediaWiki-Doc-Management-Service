from utils import run_command, load_and_check_env_vars, write_yaml_to_file, load_json_data

# Имена переменных, которые нужно загрузить
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "ANSIBLE_DIR_ABSOLUTE_PATH", "PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1: Запуск скриптов yc_service_account_configuration.py и terraform_init.py
def generate_files(path_to_script):
    """Запуск внешних python-скриптов."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)

if __name__ == '__main__':

    # Имена python-скриптов
    yc_init_script_name = "yc_service_account_configuration.py"
    terraform_init_script_name = "terraform_init.py"

    # Абсолютные пути к python-скриптам
    yc_init_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{yc_init_script_name}'
    terraform_init_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{terraform_init_script_name}'

    # Запуск python-скриптов для настройки облачного провайдера Yandex Cloud для работы с Terraform
    generate_files(yc_init_script_path)
    generate_files(terraform_init_script_path)