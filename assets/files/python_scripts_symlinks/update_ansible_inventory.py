from utils import run_command, load_and_check_env_vars, write_yaml_to_file, load_json_data
from data_handler_update_ansible_inventory import create_group_vars, get_vm_info
from ansible_structure import dynamic_groups


# Имена переменных, которые нужно загрузить
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "ANSIBLE_DIR_ABSOLUTE_PATH", \
            "PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Проверяем наличие переменных окружения и добавляем их в словарь
env_var_dic = load_and_check_env_vars(env_vars)

# Шаг 1: Cинхронизация состояния ресурсов с облачным провайдером
def terraform_data_refresh(terraform_folder_path):
    """Cинхронизация состояния ресурсов с облачным провайдером."""

    # Выполняем команды перехода в директорию и инициализации Terraform
    command = ['terraform', 'refresh']
    run_command(command, cwd=terraform_folder_path, capture_output=False)


# Шаг 2: Запуск скриптов get_terraform_vm_data.py и update_ansible_meta.py
def generate_files(path_to_script):
    """Запуск внешних python-скриптов."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)


# Шаг 3: Создание данных для будущего inventory.yaml
def create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups):
    """Создание данных для будущего inventory.yaml."""
    inventory_data = {}

    for group_name, subgroups in dynamic_groups.items():
        group_data = {
            "children": {},
            "vars": create_group_vars(ansible_meta)
        }

        for subgroup_name, subgroup_info in subgroups.items():
            subgroup_data = {"hosts": {}}
            vm_names = subgroup_info.get("hosts", [])
            external_disks = subgroup_info.get("external_disks", [])

            for vm_name in vm_names:
                if vm_name in terraform_vm_data.get("vm_ip", {}):
                    vm_info = get_vm_info(vm_name, terraform_vm_data, external_disks)
                    subgroup_data["hosts"][vm_name] = vm_info

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
