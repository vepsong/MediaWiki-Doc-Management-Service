import os
import json

# Импортируем функцию получения названия репозитория, названия папки Terraform,
# универсальную функцию для выполнения команд с проверкой результата
from utils import get_git_repo_name, find_directory_by_pattern, run_command

# Функция для создания/обновления файла параметров аутентификации
def create_ansible_meta_json(repo_name, file_name):
    # Получаем полный путь к файлу
    source_path = os.path.expanduser(f'~/{repo_name}/credentials/{file_name}')
    
    # Попытка открыть файл
    try:
        # Проверка на наличие файла и его размер
        if os.path.exists(source_path):
            if os.path.getsize(source_path) > 0:
                with open(source_path, 'r') as config_file:
                    config = json.load(config_file)
                ansible_user = config.get('ansible_user')
                ansible_password = config.get('ansible_password')

                # Если файл не содержит необходимых ключей
                if not ansible_user or not ansible_password:
                    raise ValueError("Файл пустой или содержит некорректные данные.")
                
                print(f"Файл {source_path} найден. Параметры загружены.")
                
                
                # Запрашиваем у пользователя, хочет ли он изменить данные
                choice = input("Нажмите enter, чтобы оставить текущие данные, или введите 'change', чтобы изменить их: ")
                print(f"Данные в файле {source_path} остались без изменений.")

                if choice.strip().lower() == "change":
                    raise FileNotFoundError  # Принудительно заменяем данные

            else:
                print(f"Файл {source_path} существует, но пуст.")
                raise FileNotFoundError  # Если файл пустой, выполняем ту же логику, как и при его отсутствии
        else:
            print(f"Файл {source_path} не существует.")
            raise FileNotFoundError  # Если файл не существует

    except (FileNotFoundError, ValueError):
        print(f"Файл {source_path} не найден или пуст. Создаём новый файл.")
        # Если файл не найден или пуст, запросить данные у пользователя
        print(f"Данные для подключения к ВМ")
        ansible_user = input("Введите, пожалуйста, значение ansible_user: ")
        ansible_password = input("Введите, пожалуйста, значение ansible_password: ")

        # Создаем словарь для данных
        config = {
            "ansible_user": ansible_user,
            "ansible_password": ansible_password
        }

        # Записываем данные в новый файл JSON
        with open(source_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        print(f"Файл {source_path} успешно создан.")

    except KeyError:
        print(f"Неправильный формат файла {source_path}. Параметры отсутствуют.")
        return




if __name__ == '__main__':
    file_name = "ansible_meta.json"
    repo_name = get_git_repo_name()  # Получаем имя репозитория
    create_ansible_meta_json(repo_name, file_name)
