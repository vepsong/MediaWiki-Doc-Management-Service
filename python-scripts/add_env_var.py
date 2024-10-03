import os
from utils import get_git_repo_name, find_directory_by_pattern, run_command, add_env_variable_to_bashrc


# Шаг 1. Добавление переменных окружения в ~/.bashrc
def configure_bashrc():
    # Получаем имя репозитория
    repo_name = get_git_repo_name()
    if repo_name:
        add_env_variable_to_bashrc('REPO_NAME', repo_name)

    # Получаем путь к Terraform и Ansible папкам
    terraform_relative_path, terraform_folder_name = find_directory_by_pattern(repo_name, file_extension='.tf')
    ansible_relative_path, ansible_folder_name = find_directory_by_pattern(repo_name, pattern='Ansible')

    if terraform_relative_path:
        add_env_variable_to_bashrc('TERRAFORM_RELATIVE_PATH', terraform_relative_path)
    if terraform_folder_name:
        add_env_variable_to_bashrc('TERRAFORM_FOLDER_NAME', terraform_folder_name)
    if ansible_relative_path:
        add_env_variable_to_bashrc('ANSIBLE_RELATIVE_PATH', ansible_relative_path)
    if ansible_folder_name:
        add_env_variable_to_bashrc('ANSIBLE_FOLDER_NAME', ansible_folder_name)

    # Применяем изменения
    command = ['bash', '-c', f"source ~/.bashrc"]
    run_command(command)


# Шаг 2. Проверка настроек после перезагрузки терминала
def check_env_variables():
    print("Для проверки переменных окружения перезапусти терминал и введи в командную строку следующие команды:")
    print("echo $REPO_NAME")
    print("echo $TERRAFORM_RELATIVE_PATH")
    print("echo $TERRAFORM_FOLDER_NAME")
    print("echo $ANSIBLE_RELATIVE_PATH")
    print("echo $ANSIBLE_FOLDER_NAME")


# Выполнение всех шагов
if __name__ == "__main__":
    configure_bashrc()
    check_env_variables()
