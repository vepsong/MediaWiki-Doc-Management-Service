from utils import run_command, load_and_check_env_vars

# Importing environment variables into the script
env_vars = ["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1: Running external Python scripts
def generate_files(path_to_script):
    """Running external Python scripts."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)


if __name__ == '__main__':
             
    # List of external Python scripts
    list_python_scripts_names = ["yc_service_account_configuration.py", "terraform_init.py", "update_terraform_meta.py"]

    for name in list_python_scripts_names:
        script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{name}'
        generate_files(script_path)
