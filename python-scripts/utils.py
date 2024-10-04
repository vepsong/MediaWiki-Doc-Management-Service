import subprocess
import os
import re
import json

# Функция для получения имени репозитория и путей
def get_git_repo_info():
    try:
        print("Запуск команды для получения URL репозитория...")
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if result.returncode == 0:
            repo_url = result.stdout.strip()
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            print(f"Название репозитория: {repo_name}")

            # Определение путей к репозиторию
            home_dir = os.path.expanduser("~")
            repo_relative_path = f"~/{repo_name}"  # Относительный путь с использованием '~'
            repo_path = os.path.join(home_dir, repo_name)  # Полный путь к репозиторию

            print(f"Относительный путь к репозиторию: {repo_relative_path}")
            print(f"Полный путь к репозиторию: {repo_path}")
            
            return repo_name, repo_relative_path, repo_path
        else:
            print("Ошибка при получении URL репозитория Git.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Запрашиваем ввод имени репозитория вручную, если автоматическое получение не удалось
    while True:
        manual_repo_name = input("Не удалось получить название репозитория. Хотите ввести имя вручную? (y/n): ").strip().lower()
        if manual_repo_name == 'y':
            repo_name = input("Введите название репозитория: ").strip()
            if repo_name:
                print(f"Название репозитория: {repo_name}")

                # Определение путей для ручного ввода репозитория
                home_dir = os.path.expanduser("~")
                repo_relative_path = f"~/{repo_name}"  # Относительный путь
                repo_path = os.path.join(home_dir, repo_name)  # Полный путь

                print(f"Относительный путь к репозиторию: {repo_relative_path}")
                print(f"Абсолютный путь к репозиторию: {repo_path}")
                
                return repo_name, repo_relative_path, repo_path
            else:
                print("Название репозитория не может быть пустым. Пожалуйста, введите корректное имя.")
        elif manual_repo_name == 'n':
            print("Отмена операции. Название репозитория не было получено.")
            return None, None, None
        else:
            print("Некорректный ввод. Пожалуйста, ответьте 'y' (да) или 'n' (нет).")


# Универсальная функция для поиска директории по шаблону
# Например, pattern="Ansible" или file_extension=".tf")
def find_directory_by_pattern(repo_path=None, pattern=None, file_extension=None):
    if not repo_path:
        print("Название репозитория не передано, пытаюсь получить...")
        repo_name, repo_relative_path, repo_path = get_git_repo_info()
        if not repo_path:
            print("Не удалось получить название репозитория.")
            return None, None, None
    
    # Если передан шаблон для поиска (например, 'ansible'), то компилируем его в регулярное выражение
    if pattern:
        search_pattern = re.compile(pattern, re.IGNORECASE)
    
    # Проходим по всем директориям и файлам
    for root, dirs, files in os.walk(repo_path):
        # Если передан шаблон для поиска по названию папки (например, 'ansible')
        if pattern:
            for dir_name in dirs:
                if search_pattern.search(dir_name):
                    dir_relative_path = os.path.join(root, dir_name).replace(os.path.expanduser('~'), '~')
                    dir_absolute_path = os.path.abspath(os.path.join(root, dir_name)) 
                    print(f"Название папки по шаблону '{pattern}': {dir_name}")
                    print(f"Относительный путь к папке: {dir_relative_path}")
                    print(f"Абсолютный путь к папке: {dir_absolute_path}")
                    return dir_name, dir_relative_path, dir_absolute_path
        
        # Если передано расширение файла для поиска (например, '.tf' для Terraform)
        if file_extension:
            for file in files:
                if file.endswith(file_extension):
                    folder_relative_path = root.replace(os.path.expanduser('~'), '~')  # Относительный путь
                    folder_absolute_path = os.path.abspath(root)  # Абсолютный путь к папке с файлом
                    folder_name = os.path.basename(root)
                    print(f"Название папки с файлами '{file_extension}': {folder_name}")
                    print(f"Относительный путь к папке: {folder_relative_path}")
                    print(f"Абсолютный путь к папке: {folder_absolute_path}")
                    return folder_name, folder_relative_path, folder_absolute_path
    
    print(f"Папка или файлы с шаблоном '{pattern}' или расширением '{file_extension}' не найдены в репозитории.")
    return None, None, None


# Универсальная функция для выполнения команд с проверкой результата
def run_command(command, cwd=None):
    try:
        # result = subprocess.run(command, check=True)
        result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=cwd)
        print(f"Команда '{' '.join(command)}' успешно выполнена.")
        # return result.returncode  # Возвращаем код завершения
        # print(result.returncode)
        return result.stdout # Возвращаем вывод команды
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        return e.returncode  # Возвращаем код ошибки
    
# Универсальная функция для записи данных в JSON файл
def write_json_to_file(data, file_path):
    """Записываем данные в JSON файл."""
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Файл {file_path} успешно создан.")
    except (OSError, IOError) as e:
        print(f"Ошибка при записи в файл {file_path}: {e}")

# Универсальная функция для записи данных в txt-файл
def write_txt_to_file(data, file_path):
    """Записывает текстовые данные в txt-файл."""
    try:
        with open(file_path, 'w') as txt_file:
            txt_file.write(data)
        print(f"Файл {file_path} успешно создан.")
    except (OSError, IOError) as e:
        print(f"Ошибка при записи в файл {file_path}: {e}")

# Универсальная функция для получения пути к файлу
def get_file_path(repo_name, folder_name, file_name):
    return os.path.expanduser(f'~/{repo_name}/{folder_name}/{file_name}')

# Универсальная функция для добавления переменной в bashrc
def add_env_variable_to_bashrc(variable_name, value):
    bashrc_path = os.path.expanduser('~/.bashrc')
    
    # Чтение текущего содержимого .bashrc
    with open(bashrc_path, 'r') as bashrc_file:
        lines = bashrc_file.readlines()

    # Проверка на наличие переменной и обновление её значения
    variable_found = False
    with open(bashrc_path, 'w') as bashrc_file:
        for line in lines:
            if line.startswith(f'export {variable_name}='):
                # Переменная найдена, заменяем её на новую
                bashrc_file.write(f'export {variable_name}="{value}"\n')
                variable_found = True
                print(f"Переменная окружения {variable_name} обновлена в {bashrc_path}.")
            else:
                bashrc_file.write(line)

        # Если переменная не была найдена, добавляем её в конец файла
        if not variable_found:
            bashrc_file.write(f'export {variable_name}="{value}"\n')
            print(f"Переменная окружения {variable_name} добавлена в {bashrc_path}.")


# Универсальная функция загрузки и проверки переменных окружения в python-скрипте
# Args: var_names (list): Список имен переменных окружения (напр.: env_vars = ["REPO_NAME", "REPO_PATH"])
# Returns: env_var_dic: Словарь с переменными окружения и их значениями.

def load_and_check_env_vars(var_names):

    # Загрузка переменных окружения в словарь
    env_var_dic = {var: os.environ.get(var) for var in var_names}
    
    # Проверка значений переменных окружения
    for var, value in env_var_dic.items():
        if value is None:
            print(f"Переменная окружения {var} не установлена.")
        else:
            print(f"{var}: {value}")
    
    return env_var_dic