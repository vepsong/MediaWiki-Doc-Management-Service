import json
import subprocess
import os

# Функция для получения имени репозитория из Git
def get_git_repo_name():
    try:
        # Получаем URL удалённого репозитория (origin)
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if result.returncode == 0:
            # Извлекаем URL и отделяем имя репозитория
            repo_url = result.stdout.strip()
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            return repo_name
        else:
            print("Ошибка при получении URL репозитория Git.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Если ошибка, спрашиваем пользователя вручную ввести имя репозитория
    while True:
        manual_repo_name = input("Не удалось получить имя репозитория. Хотите ввести имя вручную? (y/n): ").strip().lower()
        if manual_repo_name == 'y':
            repo_name = input("Введите имя репозитория: ").strip()
            if repo_name:
                return repo_name
            else:
                print("Имя репозитория не может быть пустым. Пожалуйста, введите корректное имя.")
        elif manual_repo_name == 'n':
            print("Отмена операции. Имя репозитория не было получено.")
            return None
        else:
            print("Некорректный ввод. Пожалуйста, ответьте 'y' (да) или 'n' (нет).")


def main():
    # Получаем имя репозитория с помощью функции
    repo_name = get_git_repo_name()
    if not repo_name:
        print("Не удалось получить имя репозитория.")
        return
    
    # Указываем относительный путь к Terraform с использованием имени репозитория
    terraform_dir = os.path.expanduser(f'~/{repo_name}/Terraform_MediaWiki')

    # Загрузка параметров аутентификации из .auth.json
    try:
        with open('.auth.json') as config_file:
            config = json.load(config_file)
        ansible_user = config['ansible_user']
        ansible_password = config['ansible_password']
    except FileNotFoundError:
        print("Файл .auth.json не найден.")
        return
    except KeyError:
        print("Неправильный формат файла .auth.json.")
        return

    # Запуск команды terraform output в указанной директории
    try:
        output = subprocess.check_output(['terraform', 'output', '-json'], cwd=terraform_dir)
        data = json.loads(output)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении Terraform: {e}")
        return
    except json.JSONDecodeError:
        print("Ошибка при разборе JSON-вывода Terraform.")
        return

    # Проверка наличия ключа vm_nat_ip и получение IP-адресов
    if 'vm_nat_ip' in data and 'value' in data['vm_nat_ip']:
        vm_nat_ip_value = data['vm_nat_ip']['value']

        # Генерация inventory.yaml
        with open('inventory.yaml', 'w') as f:
            f.write("linux: #Группа хостов\n")
            f.write("  children: #Обозначение, что будет подгруппа хостов\n")
            f.write("    nginx: #Имя подгруппы хостов\n")
            f.write("      hosts: #Узлы группы\n")

            # Итерация по IP-адресам и запись в файл
            for vm, ip in vm_nat_ip_value.items():
                host_name = f"{vm}"  # Используем имя машины
                f.write(f"        {host_name}:\n")
                f.write(f"          ansible_host: {ip}\n")

            # Добавление переменных
            f.write("  vars: #Переменные, доступные или используемые для всех подгрупп\n")
            f.write(f'    ansible_user: "{ansible_user}"\n')
            f.write(f'    ansible_password: "{ansible_password}"\n')
            f.write('    connection_protocol: ssh #тип подключения\n')
            f.write('    ansible_become: false #Становиться ли другим пользователем после подключения\n')

        print("inventory.yaml успешно сгенерирован.")

if __name__ == '__main__':
    main()
