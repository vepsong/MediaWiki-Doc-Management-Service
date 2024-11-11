import json
from utils import load_and_check_env_vars, write_json_to_file, run_command

# Importing environment variables into the script
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)


# Step 1. Terraform data synchronization with a cloud provider
def update_terraform_vm_data(terraform_folder_path):
    """Terraform data synchronization with a cloud provider."""
    command = ['terraform', 'apply', '-refresh-only']
    run_command(command, cwd=terraform_folder_path, capture_output=True)


# Step 2. Retrieving the synchronized data of VMs created through Terraform
def get_terraform_vm_data(terraform_folder_path, required_data_keys_list):
    """Retrieving the synchronized data of VMs created through Terraform (name, ip, ip-nat etc.)."""
    command = ['terraform', 'output', '-json']
    output = run_command(command, cwd=terraform_folder_path, capture_output=True)
    data = json.loads(output)
    print(data)

    # Retaining only the necessary keys
    filtered_data = {key: value["value"] for key, value in data.items() if key in required_data_keys_list}
    return filtered_data


if __name__ == '__main__':
    # Determining absolute paths to files and folders
    file_name = "terraform_vm_data.json"
    terraform_vm_data_file_in_credentials = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{file_name}'
    terraform_folder_path = env_var_dic["TERRAFORM_ABSOLUTE_PATH"]

    # Determining the list of necessary keys
    required_data_keys_list = ["vm_ip", "vm_nat_ip", "vm_boot_disk", "vm_external_disk"]

    # Updating data of VMs created through Terraform
    update_terraform_vm_data(terraform_folder_path)

    # Retrieving data of VMs created through Terraform
    terraform_vm_data = get_terraform_vm_data(terraform_folder_path, required_data_keys_list)

    # Write retrieved data to a new .json file
    write_json_to_file(terraform_vm_data, terraform_vm_data_file_in_credentials)


