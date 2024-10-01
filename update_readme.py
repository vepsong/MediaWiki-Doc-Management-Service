import re
import os

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
    # Определяем путь к текущей директории скрипта
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Используем относительные пути для файлов
    content_files = [
        (os.path.join(base_dir, 'Solution', '2.1. App deployment schema.md'), '<!-- START APP DEPLOYMENT SCHEMA -->', '<!-- END APP DEPLOYMENT SCHEMA -->'),
        (os.path.join(base_dir, 'Solution', '3.1. Service VM Docker setup.md'), '<!-- START SERVICE VM DOCKER SETUP -->', '<!-- END SERVICE VM DOCKER SETUP -->'),
        (os.path.join(base_dir, 'Solution', '3.3. YC provider setup for Terraform.md'), '<!-- START YC PROVIDER SETUP FOR TERRAFORM -->', '<!-- END YC PROVIDER SETUP FOR TERRAFORM -->')

    ]

    readme_file = os.path.join(base_dir, 'README.md')  # Относительный путь к файлу README
    update_readme(content_files, readme_file, indent='\t')  # Можно использовать '\t' для табуляции или '    ' для пробелов
