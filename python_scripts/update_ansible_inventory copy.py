from utils import run_command, load_and_check_env_vars, write_yaml_to_file, load_json_data

# Имена переменных, которые нужно загрузить
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "ANSIBLE_DIR_ABSOLUTE_PATH", \
            "PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)


# Шаг 1: Заранее определяем структуру групп и подгрупп
dynamic_groups = {
    "linuxVM": {
        "monitoringSystem": {
            "hosts": ["vm-1-monitoring-system"],
            "external_disks": [
                {
                "disk_id": "vhdd-1-monitoring-system-db",
                "mount_point": "/mnt/vhdd-1-monitoring-system-db",
                "filesystem": "ext4"
                }
            ]
        },
        "nginxProxyServer": {
            "hosts": ["vm-2-nginx-proxy-server"]
        },
        "mediawikiServer": {
            "hosts": ["vm-3-mediawiki-server-1", "vm-4-mediawiki-server-2"]
        },
        "haproxyProxyServer": {
            "hosts": ["vm-5-haproxy-proxy-server"]
        },
        "primaryDb": {
            "hosts": ["vm-6-primary-db"],
            
            "external_disks": [
                {
                "disk_id": "vssd-1-primary-db",
                "mount_point": "/mnt/vssd-1-primary-db",
                "filesystem": "ext4"
                }
            ]
        },
        "standbyDb": {
            "hosts": ["vm-7-standby-db"],
            "external_disks": [
                {
                "disk_id": "vhdd-2-standby-db",
                "mount_point": "/mnt/vhdd-2-standby-db",
                "filesystem": "ext4"
                },
                {
                "disk_id": "vhdd-3-dump-db",
                "mount_point": "/mnt/vhdd-3-dump-db",
                "filesystem": "ext4"
                }
            ]
        }   
    }
}


# Шаг 2: Cинхронизация состояния ресурсов с облачным провайдером
def terraform_data_refresh(terraform_folder_path):
    """Cинхронизация состояния ресурсов с облачным провайдером."""

    # Выполняем команды перехода в директорию и инициализации Terraform
    command = ['terraform', 'refresh']
    run_command(command, cwd=terraform_folder_path, capture_output=False)


# Шаг 3: Запуск скриптов get_terraform_vm_data.py и update_ansible_meta.py
def generate_files(path_to_script):
    """Запуск внешних python-скриптов."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)


# Шаг 4: Создание данных для будущего inventory.yaml
def create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups):
    """Создание данных для будущего inventory.yaml"""

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
        for subgroup_name, subgroup_info in subgroups.items():
            subgroup_data = {"hosts": {}}

            # Проверка на структуру данных (hosts, external_disks, mount_point и filesystem)
            vm_names = subgroup_info.get("hosts", [])
            external_disks = subgroup_info.get("external_disks", [])
            mount_points = subgroup_info.get("mount_point", None)  # None, если отсутствует
            filesystem = subgroup_info.get("filesystem", None)     # None, если отсутствует

            # Заполнение подгруппы "hosts" данными из terraform_vm_data
            for vm_name in vm_names:
                # Проверяем наличие VM в terraform_vm_data
                for key, value in terraform_vm_data.items():
                    if vm_name in value["value"]:  # Убедимся, что имя VM есть в данных
                        nat_ip = value["value"][vm_name]
                        vm_data = {
                            "ansible_host": nat_ip
                        }
                        
                        # Добавляем external_disks, если они указаны
                        if external_disks:
                            vm_data["external_disks"] = external_disks
                        
                        # Добавляем mount_points и filesystem, если они указаны
                        if mount_points:
                            vm_data["mount_point"] = mount_points
                        if filesystem:
                            vm_data["filesystem"] = filesystem
                        
                        subgroup_data["hosts"][vm_name] = vm_data

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
    terraform_folder_path = env_var_dic["TERRAFORM_ABSOLUTE_PATH"]
    
    # Абсолютный путь к файлу вывода данных
    inventory_output_file_path_ansible =f'{env_var_dic["ANSIBLE_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'
    inventory_output_file_path_credentials =f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'

    # Cинхронизация состояния ресурсов с облачным провайдером
    terraform_data_refresh(terraform_folder_path)
    
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
