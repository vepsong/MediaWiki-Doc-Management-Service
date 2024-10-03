import os
# Импортируем функцию получения названия репозитория, названия папки Terraform,
# универсальную функцию для выполнения команд с проверкой результата
from utils import get_git_repo_name, find_directory_by_pattern, run_command


def copy_terraform_config(repo_name):

    # Преобразуем пути
    source_path = os.path.expanduser(f'~/{repo_name}/credentials/{file_name}')
    destination_path = os.path.expanduser('~/')

    # Выполняем команду копирования файла .terraformrc в домашнюю директорию
    command = ['cp', source_path, destination_path]
    result = run_command(command)

    if result == 0:
        print(f"Файл конфигурации {file_name} скопирован в {destination_path}.")
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
    _, terraform_folder_name = find_directory_by_pattern(repo_name, file_extension=".tf")

    if repo_name:
        copy_terraform_config(repo_name)  # Копируем конфигурацию Terraform
        init_terraform(repo_name)  # Инициализируем Terraform
