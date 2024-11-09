from utils import get_git_repo_info, find_directory_by_pattern, run_command, add_env_variable_to_bashrc

# Step 1. Add the data from the Git repository folder to the environment variables (~/.bashrc)
def configure_bashrc_repo():
    """Add the data from the Git repository folder to the environment variables (~/.bashrc)."""
    # Get repository name
    repo_name, repo_relative_path, repo_path = get_git_repo_info()

    if repo_name:
        add_env_variable_to_bashrc('REPO_NAME', repo_name)
    if repo_relative_path:
        add_env_variable_to_bashrc('REPO_RELATIVE_PATH', repo_relative_path)
    if repo_path:
        add_env_variable_to_bashrc('REPO_PATH', repo_path)
        
    return repo_name, repo_relative_path, repo_path

# Step 2. Add the data from the Terraform folder to the environment variables (~/.bashrc)
def configure_bashrc_terraform(repo_path):
    """Add the data from the Terraform folder to the environment variables (~/.bashrc)."""

    # Get path to Terraform folder
    terraform_folder_name, terraform_folder_relative_path, \
        terraform_folder_absolute_path = find_directory_by_pattern(
            repo_path, file_extension='.tf'
        )

    if terraform_folder_name:
        add_env_variable_to_bashrc('TERRAFORM_FOLDER_NAME', terraform_folder_name)
    if terraform_folder_relative_path:
        add_env_variable_to_bashrc('TERRAFORM_RELATIVE_PATH', terraform_folder_relative_path)
    if terraform_folder_absolute_path:
        add_env_variable_to_bashrc('TERRAFORM_ABSOLUTE_PATH', terraform_folder_absolute_path)

# Step 3. Add the data from the Ansible folder to the environment variables (~/.bashrc)
def configure_bashrc_ansible(repo_path):
    """Add the data from the Ansible folder to the environment variables (~/.bashrc)."""

    # Get path to Ansible folder
    ansible_dir_name, ansible_dir_relative_path, \
        ansible_dir_absolute_path = find_directory_by_pattern(
            repo_path, pattern='Ansible'
        )

    if ansible_dir_name:
        add_env_variable_to_bashrc('ANSIBLE_DIR_NAME', ansible_dir_name)
    if ansible_dir_relative_path:
        add_env_variable_to_bashrc('ANSIBLE_DIR_RELATIVE_PATH', ansible_dir_relative_path)
    if ansible_dir_absolute_path:
        add_env_variable_to_bashrc('ANSIBLE_DIR_ABSOLUTE_PATH', ansible_dir_absolute_path)

# Step 4. Add the data from the python_scripts folder to the environment variables (~/.bashrc)
def configure_bashrc_python_scripts(repo_path):
    """Add the data from the python_scripts folder to the environment variables (~/.bashrc)."""

    # Get path to python_scripts folder
    python_scripts_dir_name, \
        python_scripts_dir_relative_path, \
        python_scripts_dir_absolute_path = \
            find_directory_by_pattern(repo_path, pattern='python_scripts')

    if python_scripts_dir_name:
        add_env_variable_to_bashrc('PYTHON_SCRIPTS_DIR_NAME', python_scripts_dir_name)
    if python_scripts_dir_relative_path:
        add_env_variable_to_bashrc('PYTHON_SCRIPTS_DIR_RELATIVE_PATH', python_scripts_dir_relative_path)
    if python_scripts_dir_absolute_path:
        add_env_variable_to_bashrc('PYTHON_SCRIPTS_DIR_ABSOLUTE_PATH', python_scripts_dir_absolute_path)


# Step 5. Add the data from the credentials folder to the environment variables (~/.bashrc)
def configure_bashrc_credentials(repo_path):
    """Add the data from the credentials folder to the environment variables (~/.bashrc)."""

    # Get path to credentials folder
    credentials_dir_name, credentials_dir_relative_path, \
        credentials_dir_absolute_path = \
            find_directory_by_pattern(repo_path, pattern='credentials')

    if credentials_dir_name:
        add_env_variable_to_bashrc('CREDENTIALS_DIR_NAME', credentials_dir_name)
    if credentials_dir_relative_path:
        add_env_variable_to_bashrc('CREDENTIALS_DIR_RELATIVE_PATH', credentials_dir_relative_path)
    if credentials_dir_absolute_path:
        add_env_variable_to_bashrc('CREDENTIALS_DIR_ABSOLUTE_PATH', credentials_dir_absolute_path)
        # Adding path to terraform_meta.txt
        add_env_variable_to_bashrc('TF_VAR_TERRAFORM_META_DIR_ABSOLUTE_PATH', f'{credentials_dir_absolute_path}/{terraform_meta_file_name}')

# Step 6. Add the data from the cYandex Cloud  to the environment variables (~/.bashrc)
def configure_bashrc_yandex_cloud():
    """Add the data from the cYandex Cloud  to the environment variables (~/.bashrc)."""
    add_env_variable_to_bashrc('YC_TOKEN', '$(yc iam create-token)')
    add_env_variable_to_bashrc('YC_CLOUD_ID', '$(yc config get cloud-id)')
    add_env_variable_to_bashrc('YC_FOLDER_ID', '$(yc config get folder-id)')



# Step 7. Apply the changes to the environment variables (~/.bashrc)
def apply_changes():
    """Apply the changes to the environment variables (~/.bashrc)."""

    command = ['bash', '-c', f"source ~/.bashrc"]
    run_command(command)


# Step 8. Verify the settings after restarting the terminal
def check_env_variables():
    print("To verify the environment variables, restart the terminal and enter the following commands in the command line:")
    print("echo $<ENVIRONMENT VARIABLE NAME>")


# Executing all steps
if __name__ == "__main__":

    terraform_meta_file_name = "terraform_meta.txt"

    repo_name, repo_relative_path, repo_path = configure_bashrc_repo()
    configure_bashrc_terraform(repo_path)
    configure_bashrc_ansible(repo_path)
    configure_bashrc_python_scripts(repo_path)
    configure_bashrc_credentials(repo_path)
    configure_bashrc_yandex_cloud()
    apply_changes()
    check_env_variables()
