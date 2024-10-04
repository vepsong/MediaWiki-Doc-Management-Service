import re
import os
# Импортируем функцию загрузки и проверки необходимых переменных окружения
from utils import load_and_check_env_vars  

# Имена переменных, которые нужно загрузить
env_vars = ["REPO_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


def add_indentation(text, indent='\t'):
    """Добавляем отступ (табуляцию) в начало каждой строки."""
    return '\n'.join(indent + line for line in text.splitlines())

def update_readme(content_files, readme_file, indent='\t'):
    # Читаем текущий файл README.md
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
   
    base_dir = env_var_dic["REPO_PATH"]
    readme_file = os.path.join(base_dir, 'README.md')  # Относительный путь к файлу README

    # Ссылки на файлы для подстановки в README.md
    content_files = [
        (os.path.join(base_dir, 'Solution', '2.1. App deployment schema.md'), '<!-- START APP DEPLOYMENT SCHEMA -->', '<!-- END APP DEPLOYMENT SCHEMA -->'),
        (os.path.join(base_dir, 'Solution', '3.1. service_vm_docker_setup.md'), '<!-- START SERVICE VM DOCKER SETUP -->', '<!-- END SERVICE VM DOCKER SETUP -->'),
        (os.path.join(base_dir, 'Solution', '3.3. preparatory_tasks.md'), '<!-- START PREPARATORY TASKS -->', '<!-- END PREPARATORY TASKS -->'),
        (os.path.join(base_dir, 'Solution', '4.3. start_pipeline.md'), '<!-- START START PIPELINE -->', '<!-- END START PIPELINE -->'),
        (os.path.join(base_dir, 'Solution', '5. ansible_setup.md'), '<!-- START ANSIBLE SETUP -->', '<!-- END ANSIBLE SETUP -->')

    ]

    update_readme(content_files, readme_file, indent='\t')  # Можно использовать '\t' для табуляции или '    ' для пробелов
