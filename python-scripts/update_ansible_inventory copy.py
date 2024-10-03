import os
import json

# Импортируем функцию получения названия репозитория, названия папки Terraform,
# универсальную функцию для выполнения команд с проверкой результата,
# универсальную функцию для записи json в файл
from utils import get_git_repo_name, find_directory_by_pattern, run_command, write_json_to_file

# Функция для создания/обновления файла параметров аутентификации
def create_ansible_meta_json(repo_name):
    # Получаем полный путь к файлу
    file_name = "ansible_meta.json"
    ansible_meta_json_file_path = (f'{credentials_path}/{file_name}')
    
    # Попытка открыть файл
    try:
        # Проверка на наличие файла и его размер
        if os.path.exists(ansible_meta_json_file_path):
            if os.path.getsize(ansible_meta_json_file_path) > 0:
                with open(ansible_meta_json_file_path, 'r') as config_file:
                    config = json.load(config_file)
                ansible_user = config.get('ansible_user')
                ansible_password = config.get('ansible_password')          
                print(f"Файл {ansible_meta_json_file_path} найден. Параметры загружены.")
                
                # Запрашиваем у пользователя, хочет ли он изменить данные
                choice = input("Нажмите enter, чтобы оставить текущие данные, или введите 'change', чтобы изменить их: ")
                print(f"Данные в файле {ansible_meta_json_file_path} остались без изменений.")

                if choice.strip().lower() == "change":
                    raise FileNotFoundError  # Принудительно заменяем данные

            else:
                print(f"Файл {ansible_meta_json_file_path} существует, но пуст.")
                raise FileNotFoundError  # Если файл пустой, выполняем ту же логику, как и при его отсутствии
        else:
            print(f"Файл {ansible_meta_json_file_path} не существует.")
            raise FileNotFoundError  # Если файл не существует

    except (FileNotFoundError, ValueError):
        print(f"Файл {ansible_meta_json_file_path} не найден или пуст. Создаём новый файл.")
        # Если файл не найден или пуст, запросить данные у пользователя
        print(f"Данные для подключения к ВМ")
        ansible_user = input("Введите, пожалуйста, значение ansible_user: ")
        ansible_password = input("Введите, пожалуйста, значение ansible_password: ")

        # Создаем словарь для данных
        data = {
            "ansible_user": ansible_user,
            "ansible_password": ansible_password
        }

        write_json_to_file(data, ansible_meta_json_file_path)

    except KeyError:
        print(f"Неправильный формат файла {ansible_meta_json_file_path}. Параметры отсутствуют.")
        return


# Получение данных созданных через Terraform ВМ
def get_terraform_vm_data(terraform_path):
                             
    command = ['terraform', 'output', '-json']
    output = run_command(command, cwd=terraform_path)
    data = json.loads(output)

    # Записываем данные в новый файл JSON
    file_name = "terraform_vm_data.json"
    terraform_vm_data_json_file_path = (f'{credentials_path}/{file_name}')

    write_json_to_file(data, terraform_vm_data_json_file_path)

if __name__ == '__main__':
    repo_name = get_git_repo_name()  # Получаем имя репозитория
    credentials_path = os.path.expanduser(f'~/{repo_name}/credentials') # Получаем путь к папке с credentials
    _, terraform_folder_name = find_directory_by_pattern(repo_name, file_extension=".tf") # Получаем название папки с файлами Terraform
    terraform_path = os.path.expanduser(f"~/{repo_name}/{terraform_folder_name}/") # Получаем путь к папке с Terraform

    create_ansible_meta_json(repo_name)
    get_terraform_vm_data(terraform_path)
