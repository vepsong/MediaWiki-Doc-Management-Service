import os
import re
from utils import load_and_check_env_vars  

# Имена переменных, которые нужно загрузить
env_vars = ["REPO_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


def get_file_names_in_directory(documentation_folder_path):
    """Получение списка всех файлов в директории."""
    # Получаем список всех файлов в директории
    list_of_file_names = [
        file_name for file_name in os.listdir(documentation_folder_path)
        if os.path.isfile(os.path.join(documentation_folder_path, file_name))
    ]
    return list_of_file_names


def add_indentation(text, indent=None):
    """Добавляем отступ (табуляцию) в начало каждой строки."""
    if indent is None:
        return text
    return '\n'.join(indent + line for line in text.splitlines())


def update_readme(content_files, readme_file, indent=None):
    """Обновление файла README.md"""
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Проходим по всем файлам и вставляем их содержимое между соответствующими метками
    for content_file, start_marker, end_marker in content_files:
        # Открываем файл с содержимым для вставки
        with open(content_file, 'r', encoding='utf-8') as f:
            new_content = f.read()

        # Добавляем табуляцию к каждой строке
        indented_content = add_indentation(new_content, indent)


        # Создаем шаблон для поиска текста между метками с захватом отступов перед метками
        pattern = re.compile(rf'{re.escape(start_marker)}.*?{re.escape(end_marker)}', re.DOTALL) 

        # Проверяем наличие меток в файле README
        if not pattern.search(readme_content):
            print(f"Метки '{start_marker}' и/или '{end_marker}' не найдены в {readme_file}. Пропускаем.")
            continue

        # Обновляем содержимое README.md с добавленной табуляцией
        readme_content = pattern.sub(f'{start_marker}\n{indented_content}\n{end_marker}', readme_content)

    # Записываем обновленное содержимое обратно в README.md
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"{readme_file} успешно обновлен.")


if __name__ == "__main__":

    repo_dir = f'{env_var_dic["REPO_PATH"]}'

    documentation_folder_name = "project_documentation"
    documentation_folder_path = f'{repo_dir}/{documentation_folder_name}'

    readme_file_name = 'README.md'
    readme_file_path = f'{repo_dir}/{readme_file_name}'

    list_of_file_names = get_file_names_in_directory(documentation_folder_path)

    for name in list_of_file_names:
        content_files = [
            (f'{documentation_folder_path}/{name}', f'<!-- START_{name} -->', f'<!-- END_{name} -->'),
        ]

        # update_readme(content_files, readme_file_path, indent='\t')
        update_readme(content_files, readme_file_path, indent=None)
