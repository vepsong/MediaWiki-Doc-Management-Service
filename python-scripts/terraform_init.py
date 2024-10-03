import os
import subprocess
# Импортируем функцию получения имени репозитория и пути к папке Terraform
from utils import get_git_repo_name, find_terraform_directory


def copy_terraform_config(repo_name):
    # Выполняем команду копирования файла .terraformrc в домашнюю директорию
    command = f'cp ~/{repo_name}/credentials/{file_name} ~/'
    result = os.system(command)
    if result == 0:
        print(f"Файл конфигурации {file_name} скопирован в {os.path.expanduser(f'~/')}.")
    else:
        print("Ошибка копирования файла конфигурации.")


def init_terraform(repo_name):
    # Выполняем команды перехода в директорию и инициализации Terraform
    command = f'cd ~/{repo_name}/{terraform_folder_name} && terraform init'
    result = os.system(command)

    if result == 0:
        print("Terraform инициализирован успешно.")
    else:
        print("Ошибка инициализации Terraform.")


if __name__ == "__main__":
    repo_name = get_git_repo_name()  # Получаем имя репозитория
    file_name = ".terraformrc"
    _, terraform_folder_name = find_terraform_directory(repo_name)

    if repo_name:
        copy_terraform_config(repo_name)  # Копируем конфигурацию Terraform
        init_terraform(repo_name)  # Инициализируем Terraform
