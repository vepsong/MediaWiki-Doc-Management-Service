from utils import get_git_repo_info, find_directory_by_pattern, run_command, add_env_variable_to_bashrc


# Шаг 1. Добавление данных папки git-репозитория в переменные окружения (~/.bashrc)
def configure_bashrc_repo():
    """Добавление данных папки git-репозитория в переменные окружения (~/.bashrc)."""
    # Получаем имя репозитория
    repo_name, repo_relative_path, repo_path = get_git_repo_info()

    if repo_name:
        add_env_variable_to_bashrc('REPO_NAME', repo_name)
    if repo_relative_path:
        add_env_variable_to_bashrc('REPO_RELATIVE_PATH', repo_relative_path)
    if repo_path:
        add_env_variable_to_bashrc('REPO_PATH', repo_path)
        
    return repo_name, repo_relative_path, repo_path

# Шаг 2. Добавление данных папки Terraform в переменные окружения (~/.bashrc)
def configure_bashrc_terraform(repo_path):
    """Добавление данных папки Terraform в переменные окружения (~/.bashrc)."""

    # Получаем путь к папке Terraform
    terraform_folder_name, terraform_folder_relative_path, \
        terraform_folder_absolute_path = find_directory_by_pattern(
            repo_path, file_extension='.tf'
        )

    if terraform_folder_name:
        add_env_variable_to_bashrc('TERRAFORM_FOLDER_NAME', terraform_folder_name)
    if terraform_folder_relative_path:
        add_env_variable_to_bashrc('TERRAFORM_RELATIVE_PATH', terraform_folder_relative_path)
    if terraform_folder_absolute_path:
        add_env_variable_to_bashrc('TERRAFORM_ABSOLUTE_PATH', terraform_folder_absolute_path)


# Шаг 3. Добавление данных папки Ansible в переменные окружения (~/.bashrc)
def configure_bashrc_ansible(repo_path):
    """Добавление данных папки Ansible в переменные окружения (~/.bashrc)."""

    # Получаем путь к папке Ansible
    ansible_dir_name, ansible_dir_relative_path, \
        ansible_dir_absolute_path = find_directory_by_pattern(
            repo_path, pattern='Ansible'
        )

    if ansible_dir_name:
        add_env_variable_to_bashrc('ANSIBLE_DIR_NAME', ansible_dir_name)
    if ansible_dir_relative_path:
        add_env_variable_to_bashrc('ANSIBLE_DIR_RELATIVE_PATH', ansible_dir_relative_path)
    if ansible_dir_absolute_path:
        add_env_variable_to_bashrc('ANSIBLE_DIR_ABSOLUTE_PATH', ansible_dir_absolute_path)


# Шаг 4. Добавление данных папки python-scripts в переменные окружения (~/.bashrc)
def configure_bashrc_python_scripts(repo_path):
    """Добавление данных папки python-scripts в переменные окружения (~/.bashrc)."""

    # Получаем путь к папке python-scripts
    python_scripts_dir_name, \
        python_scripts_dir_relative_path, \
        python_scripts_dir_absolute_path = \
            find_directory_by_pattern(repo_path, pattern='python-scripts')

    if python_scripts_dir_name:
        add_env_variable_to_bashrc('PYTHON_SCRIPTS_DIR_NAME', python_scripts_dir_name)
    if python_scripts_dir_relative_path:
        add_env_variable_to_bashrc('PYTHON_SCRIPTS_DIR_RELATIVE_PATH', python_scripts_dir_relative_path)
    if python_scripts_dir_absolute_path:
        add_env_variable_to_bashrc('PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH', python_scripts_dir_absolute_path)


# Шаг 5. Добавление данных папки credentials в переменные окружения (~/.bashrc)
def configure_bashrc_credentials(repo_path):
    """Добавление данных папки credentials в переменные окружения (~/.bashrc)."""

    # Получаем путь к папке credentials
    credentials_dir_name, credentials_dir_relative_path, \
        credentials_dir_absolute_path = \
            find_directory_by_pattern(repo_path, pattern='credentials')

    if credentials_dir_name:
        add_env_variable_to_bashrc('CREDENTIALS_DIR_NAME', credentials_dir_name)
    if credentials_dir_relative_path:
        add_env_variable_to_bashrc('CREDENTIALS_DIR_RELATIVE_PATH', credentials_dir_relative_path)
    if credentials_dir_absolute_path:
        add_env_variable_to_bashrc('CREDENTIALS_DIR_ABSOLUTE_PATH', credentials_dir_absolute_path)


# Шаг 6. Добавление данных Yandex Cloud в переменные окружения (~/.bashrc)
def configure_bashrc_yandex_cloud():
    """Добавление данных Yandex Cloud в переменные окружения (~/.bashrc)."""
    add_env_variable_to_bashrc('YC_TOKEN', '$(yc iam create-token)')
    add_env_variable_to_bashrc('YC_CLOUD_ID', '$(yc config get cloud-id)')
    add_env_variable_to_bashrc('YC_FOLDER_ID', '$(yc config get folder-id)')



# Шаг 7. Применение изменений в переменных окружения (~/.bashrc)
def apply_changes():
    """Применение изменений в переменных окружения (~/.bashrc)."""

    command = ['bash', '-c', f"source ~/.bashrc"]
    run_command(command)


# Шаг 8. Проверка настроек после перезагрузки терминала
def check_env_variables():
    print("Для проверки переменных окружения перезапусти терминал и введи в командную строку следующие команды:")
    print("echo $<ИМЯ ПЕРЕМЕННОЙ ОКРУЖЕНИЯ>")


# Выполнение всех шагов
if __name__ == "__main__":
    repo_name, repo_relative_path, repo_path = configure_bashrc_repo()
    configure_bashrc_terraform(repo_path)
    configure_bashrc_ansible(repo_path)
    configure_bashrc_python_scripts(repo_path)
    configure_bashrc_credentials(repo_path)
    configure_bashrc_yandex_cloud()
    apply_changes()
    check_env_variables()
