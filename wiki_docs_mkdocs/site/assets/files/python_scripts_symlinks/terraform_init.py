import os
from utils import run_command, load_and_check_env_vars, copy_file

# Importing environment variables into the script
env_vars = ["CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)


# Step 1: Terraform initialization
def terraform_init(terraform_folder_path):
    """Terraform initialization."""

    # Running Terraform initialization command
    command = ['terraform', 'init']
    run_command(command, cwd=terraform_folder_path, capture_output=False)


if __name__ == "__main__":
    user_home_path = os.path.expanduser('~/')
    provider_conf_file_name = ".terraformrc"
    provider_conf_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{provider_conf_file_name}'
    terraform_folder_path = f'{env_var_dic["TERRAFORM_ABSOLUTE_PATH"]}'

    # Copy of provider configuration
    copy_file(provider_conf_file_path, user_home_path)
    # Terraform initializatio
    terraform_init(terraform_folder_path)