# Импортируем необходимые библиотеки
import os
# Импортируем функцию загрузки и проверки необходимых переменных окружения, записи данных в txt-файл
from utils import load_and_check_env_vars, write_json_to_file

# Имена переменных, которые нужно загрузить
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1. Формирование содержимого для файла ansible_meta.json
def create_ansible_meta_content():
    """Создает содержимое для файла ansible_meta.json."""
    try:
        # Спрашиваем у пользователя, хочет ли он оставить данные по умолчанию или изменить их
        choice = input("Нажмите enter, чтобы оставить данные по-умолчанию, или введите 'change', чтобы изменить их: ").strip().lower()

        if choice == 'change':
            # Запрашиваем пользовательские значения
            print("Пустой ввод оставит значение поля по-умолчанию")
            ansible_user = input("Введите значение для 'ansible_user' (default: root): ") or "root"
            ansible_password = input("Введите значение для 'ansible_password' (default: ""): ") or ""
        else:
            # Используем значения по умолчанию
            ansible_user = "root"
            ansible_password = ""

        data = {
            "ansible_user": ansible_user,
            "ansible_password": ansible_password
        }
        return data
    except Exception as e:
        print(f"Произошла ошибка при формировании содержимого файла: {e}")
        exit(1)


if __name__ == "__main__":
    # Определение абсолютных путей к файлам и папкам
    file_name = "ansible_meta.json"
    meta_file_in_credentials = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{file_name}'

    # Формирование данных для записи в файл
    ansible_meta_content = create_ansible_meta_content() 

    # Запись содержимого в файл "ansible_meta.json"
    write_json_to_file(ansible_meta_content, meta_file_in_credentials) 
