from utils import run_command, load_and_check_env_vars, load_json_data

# Importing environment variables into the script
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)

# Step 1. Creating a file with Yandex Cloud service account authentication data (for use with Terraform)
def create_service_yc_account_ssh_key(yc_meta_file_data, yc_meta_key_file_path):
    """Creating a file with Yandex Cloud service account authentication data (for use with Terraform)."""
    
    service_account_id = yc_meta_file_data['service_account_id']

    command = [
        'yc', 'iam', 'key', 'create',
        '--service-account-id', service_account_id,
        '--folder-name', 'default',
        '--output', yc_meta_key_file_path
    ]
    run_command(command)


# Step 2. Creating a local YC profile
def create_yc_profile(yc_meta_file_data):
    """Creating a local YC profile."""

    profile_name = yc_meta_file_data['profile-name']

    print(f"Profile creation for {profile_name}...")
    command = ['yc', 'config', 'profile', 'create', profile_name]
    run_command(command)


# Step 3. Setting up the local YC profile
def configure_yc_profile(yc_meta_file_data, yc_meta_key_file_path):
    """Setting up the local YC profile."""
    
    profile_name = yc_meta_file_data['profile-name']
    cloud_id = yc_meta_file_data['cloud-id']
    folder_id = yc_meta_file_data['folder-id']

    print(f"Setting up the local YC profile for {profile_name}...")

    # Setting up the SSH key for the local YC service account
    command_profile = ['yc', 'config', 'set', 'service-account-key', yc_meta_key_file_path]
    run_command(command_profile)

    # Setting up the Cloud ID and Folder ID
    command_cloud_id = ['yc', 'config', 'set', 'cloud-id', cloud_id]
    command_folder_id = ['yc', 'config', 'set', 'folder-id', folder_id]
    run_command(command_cloud_id)
    run_command(command_folder_id)


# Executing all the steps
if __name__ == "__main__":

    # Name of the metadata file.
    yc_meta_file = "yc_meta.json"

    # Name of the output file with data
    yc_meta_key_file = "key.json"

    # Absolute path to the data files
    yc_meta_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{yc_meta_file}'
    yc_meta_key_file_path = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{yc_meta_key_file}'

    # Retrieving content from the 'yc_meta.json' file
    yc_meta_file_data = load_json_data(yc_meta_file_path)
    # Creating a file with Yandex Cloud service account authentication data (for use with Terraform)
    create_service_yc_account_ssh_key(yc_meta_file_data, yc_meta_key_file_path)
    # Creating a local YC profile
    create_yc_profile(yc_meta_file_data)
    # Setting up the local YC profile
    configure_yc_profile(yc_meta_file_data, yc_meta_key_file_path)
