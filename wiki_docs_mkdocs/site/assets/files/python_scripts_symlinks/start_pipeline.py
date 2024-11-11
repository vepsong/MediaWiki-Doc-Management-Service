from utils import run_command, load_and_check_env_vars

# Имена переменных, которые нужно загрузить
env_vars = ["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1: Запуск скриптов yc_service_account_configuration.py и terraform_init.py
def generate_files(path_to_script):
    """Запуск внешних python-скриптов."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)


if __name__ == '__main__':
             
    # Список названий python-скриптов 
    list_python_scripts_names = ["yc_service_account_configuration.py", "terraform_init.py", "update_terraform_meta.py"]

    for name in list_python_scripts_names:
        script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{name}'
        generate_files(script_path)
