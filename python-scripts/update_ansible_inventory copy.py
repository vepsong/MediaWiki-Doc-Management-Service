import json
import subprocess
import os

# Импортируем функцию получения названия репозитория, названия папки Terraform,
# универсальную функцию для выполнения команд с проверкой результата
from utils import get_git_repo_name, find_directory_by_pattern, run_command



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
    file_name = "ansible_meta.json"
    repo_name = get_git_repo_name()  # Получаем имя репозитория
    _, terraform_folder_name = find_directory_by_pattern(repo_name, file_extension=".tf") # получаем название папки с Terraform
    create_ansible_meta_json(repo_name, file_name)
