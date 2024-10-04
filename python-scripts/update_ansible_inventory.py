import json
from utils import run_command, load_and_check_env_vars, write_yaml_to_file

# Имена переменных, которые нужно загрузить
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "ANSIBLE_DIR_ABSOLUTE_PATH", "PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Заранее определяем структуру групп и подгрупп
dynamic_groups = {
    "linux": {
        "nginx": ["vm-2", "vm-3"],
        "database": ["vm-4"]
    },
    "windows": {
        "web_servers": ["vm-5"],
        "app_servers": ["vm-6"]
    }
}

# Шаг 1: Запуск скриптов get_terraform_vm_data.py и update_ansible_meta.py
def generate_files(path_to_script):
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)

# Шаг 2: Загрузка данных из JSON-файлов
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups):
    inventory_data = {}

    # Добавляем группы и подгруппы из dynamic_groups
    for group_name, subgroups in dynamic_groups.items():
        group_data = {
            "children": {},
            "vars": {
                "ansible_user": ansible_meta.get("ansible_user"),
                "ansible_password": ansible_meta.get("ansible_password"),
                "connection_protocol": ansible_meta.get("connection_protocol"),
                "ansible_become": ansible_meta.get("ansible_become")
            }
        }

        # Создаем подгруппы и добавляем хосты из terraform_vm_data
        for subgroup_name, vm_names in subgroups.items():
            subgroup_data = {"hosts": {}}

            # Заполнение подгруппы "hosts" данными из terraform_vm_data
            for vm_name in vm_names:
                # Проверяем наличие VM в terraform_vm_data
                for key, value in terraform_vm_data.items():
                    if vm_name in value["value"]:  # Убедимся, что имя VM есть в данных
                        nat_ip = value["value"][vm_name]
                        subgroup_data["hosts"][vm_name] = {"ansible_host": nat_ip}

            group_data["children"][subgroup_name] = subgroup_data

        inventory_data[group_name] = group_data

    return inventory_data


if __name__ == '__main__':

    # Имена python-скриптов
    ansible_meta_script = "update_ansible_meta.py"
    terraform_vm_data_script = "get_terraform_vm_data.py"

    # Имена файлов с данными
    ansible_meta_file = "ansible_meta.json"
    terraform_vm_data_file = "terraform_vm_data.json"
    
    # Имя файла вывода с данными
    inventory_output_file = "inventory.yaml"

    # Абсолютные пути к python-скриптам
    ansible_meta_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{ansible_meta_script}'
    terraform_vm_data_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{terraform_vm_data_script}'

    # Абсолютные пути к файлам данных
    ansible_meta_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{ansible_meta_file}'
    terraform_vm_data_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{terraform_vm_data_file}'
    
    # Абсолютный путь к файлу вывода данных
    inventory_output_file_path_ansible =f'{env_var_dic["ANSIBLE_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'
    inventory_output_file_path_credentials =f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'

    # Запуск python-скриптов для генерации файлов "ansible_meta.json" и "terraform_vm_data.json"
    generate_files(ansible_meta_script_path)
    generate_files(terraform_vm_data_script_path)

    # Загрузка данных из JSON-файлов
    ansible_meta = load_json_data(ansible_meta_file_path)
    terraform_vm_data = load_json_data(terraform_vm_data_file_path)

    # Формирование данных для inventory.yaml
    inventory_data = create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups)

    # Запись данных в inventory.yaml
    write_yaml_to_file(inventory_data, inventory_output_file_path_ansible)
    write_yaml_to_file(inventory_data, inventory_output_file_path_credentials)