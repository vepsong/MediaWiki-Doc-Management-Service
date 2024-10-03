import subprocess
import os
import re

# Функция для получения имени репозитория
def get_git_repo_name():
    try:
        print("Запуск команды для получения URL репозитория...")
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if result.returncode == 0:
            repo_url = result.stdout.strip()
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            print(f"Название репозитория: {repo_name}")
            return repo_name
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
                return repo_name
            else:
                print("Название репозитория не может быть пустым. Пожалуйста, введите корректное имя.")
        elif manual_repo_name == 'n':
            print("Отмена операции. Название репозитория не было получено.")
            return None
        else:
            print("Некорректный ввод. Пожалуйста, ответьте 'y' (да) или 'n' (нет).")


# Универсальная функция для поиска директории по шаблону
# Например, pattern="Ansible" или file_extension=".tf")
def find_directory_by_pattern(repo_name=None, pattern=None, file_extension=None):
    if not repo_name:
        print("Название репозитория не передано, пытаюсь получить...")
        repo_name = get_git_repo_name()
        if not repo_name:
            print("Не удалось получить название репозитория.")
            return None, None
    
    # Получаем полный путь до репозитория
    repo_path = os.path.expanduser(f"~/{repo_name}")
    
    # Если передан шаблон для поиска (например, 'ansible'), то компилируем его в регулярное выражение
    if pattern:
        search_pattern = re.compile(pattern, re.IGNORECASE)
    
    # Проходим по всем директориям и файлам
    for root, dirs, files in os.walk(repo_path):
        # Если передан шаблон для поиска по названию папки (например, 'ansible')
        if pattern:
            for dir_name in dirs:
                if search_pattern.search(dir_name):
                    relative_path = os.path.join(root, dir_name).replace(os.path.expanduser('~'), '~')
                    print(f"Название папки по шаблону '{pattern}': {dir_name}")
                    print(f"Относительный путь к папке: {relative_path}")
                    return relative_path, dir_name
        
        # Если передано расширение файла для поиска (например, '.tf' для Terraform)
        if file_extension:
            for file in files:
                if file.endswith(file_extension):
                    relative_path = root.replace(os.path.expanduser('~'), '~')
                    folder_name = os.path.basename(root)
                    print(f"Название папки с файлами '{file_extension}': {folder_name}")
                    print(f"Относительный путь к папке: {relative_path}")
                    return relative_path, folder_name
    
    print(f"Папка или файлы с шаблоном '{pattern}' или расширением '{file_extension}' не найдены в репозитории.")
    return None, None


# Универсальная функция для выполнения команд с проверкой результата
def run_command(command):
    try:
        result = subprocess.run(command, check=True)
        print(f"Команда '{' '.join(command)}' успешно выполнена.")
        return result.returncode  # Возвращаем код завершения
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        return e.returncode  # Возвращаем код ошибки

