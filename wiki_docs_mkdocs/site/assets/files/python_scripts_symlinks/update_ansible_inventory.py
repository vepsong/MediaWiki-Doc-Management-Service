from utils import run_command, load_and_check_env_vars, write_yaml_to_file, load_json_data
from data_handler_update_ansible_inventory import create_group_vars, get_vm_info
from ansible_structure import dynamic_groups


# Importing environment variables into the script
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "ANSIBLE_DIR_ABSOLUTE_PATH", \
            "PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)


# # Step 1. Terraform data synchronization with a cloud provider
# def terraform_data_refresh(terraform_folder_path):
#     """Terraform data synchronization with a cloud provider."""

#     command = ['terraform', 'apply', '-refresh-only']
#     run_command(command, cwd=terraform_folder_path, capture_output=False)


# Step 1: Running external Python scripts
def generate_files(path_to_script):
    """Running external Python scripts."""
    comand = ["python3", path_to_script]
    run_command(comand, capture_output=False)


# Step 2: Data creation for inventory.yaml
def create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups):
    """Data creation for inventory.yaml."""
    inventory_data = {}

    for group_name, subgroups in dynamic_groups.items():
        group_data = {
            "children": {},
            "vars": create_group_vars(ansible_meta)
        }

        for subgroup_name, subgroup_info in subgroups.items():
            subgroup_data = {"hosts": {}}
            vm_names = subgroup_info.get("hosts", [])
            external_disks = subgroup_info.get("external_disks", {})
            # external_disks = subgroup_info.get("external_disks", [])
            print(f"Debugging subgroup_info: {subgroup_info}")
            
            for vm_name in vm_names:

                    vm_external_disks = external_disks.get(vm_name, [])
                    vm_info = get_vm_info(vm_name, terraform_vm_data, vm_external_disks)
                    subgroup_data["hosts"][vm_name] = vm_info

            group_data["children"][subgroup_name] = subgroup_data

        inventory_data[group_name] = group_data

    return inventory_data



if __name__ == '__main__':

    # Python scripts names
    ansible_meta_script = "update_ansible_meta.py"
    terraform_vm_data_script = "get_terraform_vm_data.py"

    # Data files names
    ansible_meta_file = "ansible_meta.json"
    terraform_vm_data_file = "terraform_vm_data.json"
    
    # Output data file name
    inventory_output_file = "inventory.yaml"

    # Absolute paths to Python scripts
    ansible_meta_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{ansible_meta_script}'
    terraform_vm_data_script_path = f'{env_var_dic["PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH"]}/{terraform_vm_data_script}'

    # Absolute paths to data files
    ansible_meta_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{ansible_meta_file}'
    terraform_vm_data_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{terraform_vm_data_file}'
    terraform_folder_path = env_var_dic["TERRAFORM_ABSOLUTE_PATH"]

    # Absolute paths to output data file
    inventory_output_file_path_ansible =f'{env_var_dic["ANSIBLE_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'
    inventory_output_file_path_credentials =f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{inventory_output_file}'

    # # Terraform data synchronization with a cloud provider
    # terraform_data_refresh(terraform_folder_path)
    
    # Running external Python scripts to generate: "ansible_meta.json" and "terraform_vm_data.json"
    generate_files(ansible_meta_script_path)
    generate_files(terraform_vm_data_script_path)


    # Data loading from JSON files
    ansible_meta = load_json_data(ansible_meta_file_path)
    terraform_vm_data = load_json_data(terraform_vm_data_file_path)

    # Data creation inventory.yaml
    inventory_data = create_inventory_data(ansible_meta, terraform_vm_data, dynamic_groups)

    # save data to inventory.yaml
    write_yaml_to_file(inventory_data, inventory_output_file_path_ansible)
    write_yaml_to_file(inventory_data, inventory_output_file_path_credentials)
