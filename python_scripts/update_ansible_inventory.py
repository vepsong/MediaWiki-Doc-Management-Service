from utils import run_command, load_and_check_env_vars, write_yaml_to_file, load_json_data

# Имена переменных, которые нужно загрузить
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "ANSIBLE_DIR_ABSOLUTE_PATH", \
            "PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1: Заранее определяем структуру групп и подгрупп
dynamic_groups = {
    "linux_vm": {
        "monitoring-system": ["vm-1-monitoring-system", "vm-1"],
        "nginx-proxy-server": ["vm-2-proxy-server"],
        "mediawiki-server": ["vm-3-mediawiki-server-1",
                            "vm-4-mediawiki-server-2"],
        "haproxy-proxy-server": ["vm-5-haproxy-proxy-server"],
        "primary-db": ["vm-6-primary-db"],
        "standby-db": ["vm-7-standby-db"]
    },

    "external_storage": {
        "storage-monitoring-system-db": ["vhdd-1-monitoring-system-db"],
        "storage-standby-db": ["vhdd-2-standby-db"],
        "storage-dump-db": ["vhdd-3-dump-db"],
        "storage-primary-db": ["vssd-1-primary-db"]
    }
}


# Шаг 2: Cинхронизация состояния ресурсов с облачным провайдером
def terraform_data_refresh(terraform_folder_path):
    """Cинхронизация состояния ресурсов с облачным провайдером."""

    # Выполняем команды перехода в директорию и инициализации Terraform
    command = ['terraform', 'refresh']
    run_command(command, cwd=terraform_folder_path, capture_output=False)


# Шаг 3: Запуск скриптов update_ansible_meta.py
def generate_files(path_to_script):
    """Запуск внешних python-скриптов."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)


def parse_terraform_state(tfstate):
    """Извлекает информацию о VM из terraform.tfstate"""
    vm_data = {}
    for resource in tfstate['resources']:
        if resource['type'] == 'yandex_compute_instance':  # проверьте нужный тип ресурса
            for instance in resource['instances']:
                attributes = instance['attributes']
                name = attributes.get('name')
                if name:
                    network_interfaces = attributes.get('network_interface', [{}])
                    nat_ip = network_interfaces[0].get('nat_ip_address')
                    if nat_ip:
                        vm_data[name] = {"nat_ip_address": nat_ip}
    return vm_data


# Шаг 4: Создание данных для будущего inventory.yaml
def create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups):
    """Создание данных для будущего inventory.yaml"""

    inventory_data = {}

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

        for subgroup_name, vm_names in subgroups.items():
            subgroup_data = {"hosts": {}}

            for vm_name in vm_names:
                # Поиск VM в terraform_vm_data по имени и добавление её IP или пустого значения
                vm_info = terraform_vm_data.get(vm_name)
                nat_ip = vm_info["nat_ip_address"] if vm_info and "nat_ip_address" in vm_info else ""
                
                # Добавляем виртуальную машину с NAT IP или пустым значением
                subgroup_data["hosts"][vm_name] = {"ansible_host": nat_ip}

            group_data["children"][subgroup_name] = subgroup_data

        inventory_data[group_name] = group_data

    return inventory_data



if __name__ == '__main__':

    # Имена python-скриптов
    ansible_meta_script = "update_ansible_meta.py"

    # Имена файлов с данными
    ansible_meta_file = "ansible_meta.json"
    terraform_tfstate_file = "terraform.tfstate"
    
    # Имя файла вывода с данными
    inventory_output_file = "inventory.yaml"

    # Абсолютные пути к python-скриптам
    ansible_meta_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{ansible_meta_script}'

    # Абсолютные пути к файлам данных
    ansible_meta_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{ansible_meta_file}'
    terraform_vm_data_file_path = f'{env_var_dic["TERRAFORM_ABSOLUTE_PATH"]}/{terraform_tfstate_file}'
    terraform_folder_path = env_var_dic["TERRAFORM_ABSOLUTE_PATH"]
    
    # Абсолютный путь к файлу вывода данных
    inventory_output_file_path_ansible =f'{env_var_dic["ANSIBLE_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'
    inventory_output_file_path_credentials =f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'

    # Cинхронизация состояния ресурсов с облачным провайдером
    terraform_data_refresh(terraform_folder_path)
    
    # Запуск python-скриптов для генерации файлов "ansible_meta.json"
    generate_files(ansible_meta_script_path)


    # Загрузка данных из JSON-файлов
    ansible_meta = load_json_data(ansible_meta_file_path)
    terraform_vm_data = load_json_data(terraform_vm_data_file_path)


    # Формирование данных для inventory.yaml
    inventory_data = create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups)


    # Запись данных в inventory.yaml
    write_yaml_to_file(inventory_data, inventory_output_file_path_ansible)
    write_yaml_to_file(inventory_data, inventory_output_file_path_credentials)
