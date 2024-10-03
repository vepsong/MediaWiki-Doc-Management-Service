import subprocess
import os


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




# Функция для поиска папки с Terraform и возвращения полного пути и названия папки
def find_terraform_directory(repo_name=None):
    if not repo_name:
        print("Название репозитория не передано, пытаюсь получить...")
        repo_name = get_git_repo_name()
        if not repo_name:
            print("Не удалось получить название репозитория.")
            return None, None
    
    # Получаем полный путь до репозитория
    repo_path = os.path.expanduser(f"~/{repo_name}")
    
    # Проходим по всем папкам и ищем файлы .tf
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.tf'):
                # Заменяем путь до домашней директории на ~
                terraform_relative_path = root.replace(os.path.expanduser('~'), '~')
                # Получаем просто имя папки
                terraform_folder_name = os.path.basename(root)
                print(f"Название папки terraform: {terraform_folder_name}")
                print(f"Относительный путь к папке terraform: {terraform_relative_path}")
                return terraform_relative_path, terraform_folder_name
    
    print("Файлы Terraform (.tf) не найдены в репозитории.")
    return None, None


# Универсальная функция для выполнения команд с проверкой результата
def run_command(command):
    try:
        subprocess.run(command, check=True)
        print(f"Команда '{' '.join(command)}' успешно выполнена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
