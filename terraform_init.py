import os
import subprocess


def get_git_repo_name():
    try:
        # Получаем URL удалённого репозитория (origin)
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if result.returncode == 0:
            # Извлекаем URL и отделяем имя репозитория
            repo_url = result.stdout.strip()
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            return repo_name
        else:
            print("Ошибка при получении URL репозитория Git.")
            return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def copy_terraform_config(repo_name):
    # Выполняем команду копирования файла .terraformrc в домашнюю директорию
    command = f'cp ~/{repo_name}/Terraform_MediaWiki/.terraformrc ~/'
    result = os.system(command)
    if result == 0:
        print("Файл конфигурации .terraformrc скопирован в домашнюю директорию.")
    else:
        print("Ошибка копирования файла конфигурации.")


def init_terraform(repo_name):
    # Выполняем команды перехода в директорию и инициализации Terraform
    command = f'cd {repo_name}/Terraform_MediaWiki && terraform init'
    result = os.system(command)

    if result == 0:
        print("Terraform инициализирован успешно.")
    else:
        print("Ошибка инициализации Terraform.")


if __name__ == "__main__":
    repo_name = get_git_repo_name()  # Получаем имя репозитория
    if repo_name:
        print(f"Имя репозитория: {repo_name}")
        copy_terraform_config(repo_name)  # Копируем конфигурацию Terraform
        init_terraform(repo_name)  # Инициализируем Terraform
