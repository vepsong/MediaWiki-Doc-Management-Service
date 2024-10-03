import os
import json
from utils import get_git_repo_name, find_directory_by_pattern, run_command, write_json_to_file, get_file_path


# Функция для запроса данных у пользователя Ansible
def request_ansible_credentials():
    print("Данные для подключения к ВМ:")
    ansible_user = input("Введите, пожалуйста, значение ansible_user: ")
    ansible_password = input("Введите, пожалуйста, значение ansible_password: ")
    return {"ansible_user": ansible_user, "ansible_password": ansible_password}


# Функция для создания/обновления файла параметров аутентификации
def create_ansible_meta_json(repo_name, credentials_path):
    ansible_meta_json_file_path = get_file_path(repo_name, 'credentials', 'ansible_meta.json')

    try:
        # Если файл существует и не пустой
        if os.path.exists(ansible_meta_json_file_path) and os.path.getsize(ansible_meta_json_file_path) > 0:
            with open(ansible_meta_json_file_path, 'r') as config_file:
                config = json.load(config_file)
            ansible_user = config.get('ansible_user')
            ansible_password = config.get('ansible_password')
            print(f"Файл {ansible_meta_json_file_path} найден. Параметры загружены.")

            # Проверка, хочет ли пользователь заменить данные
            choice = input("Нажмите enter, чтобы оставить текущие данные, или введите 'change', чтобы изменить их: ")
            if choice.strip().lower() == "change":
                raise FileNotFoundError

        else:
            print(f"Файл {ansible_meta_json_file_path} существует, но пуст.")
            raise FileNotFoundError

    except (FileNotFoundError, ValueError):
        print(f"Файл {ansible_meta_json_file_path} не найден или пуст. Создаём новый файл.")
        data = request_ansible_credentials()
        write_json_to_file(data, ansible_meta_json_file_path)

    except KeyError:
        print(f"Неправильный формат файла {ansible_meta_json_file_path}. Параметры отсутствуют.")
        return


# Получение данных созданных через Terraform ВМ
def get_terraform_vm_data(terraform_path, credentials_path):
    command = ['terraform', 'output', '-json']
    output = run_command(command, cwd=terraform_path)
    data = json.loads(output)

    # Записываем данные в новый файл JSON
    terraform_vm_data_json_file_path = get_file_path(credentials_path, '', 'terraform_vm_data.json')
    write_json_to_file(data, terraform_vm_data_json_file_path)


if __name__ == '__main__':
    repo_name = get_git_repo_name()  # Получаем имя репозитория
    credentials_path = get_file_path(repo_name, 'credentials', '')  # Путь к папке с credentials
    _, terraform_folder_name = find_directory_by_pattern(repo_name, file_extension=".tf")  # Получаем название папки с файлами Terraform
    terraform_path = get_file_path(repo_name, terraform_folder_name, '')  # Путь к папке с Terraform

    create_ansible_meta_json(repo_name, credentials_path)
    get_terraform_vm_data(terraform_path, credentials_path)
