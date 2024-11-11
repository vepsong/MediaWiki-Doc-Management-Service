import os
from utils import load_and_check_env_vars, write_txt_to_file

# Importing environment variables into the script
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)


# Step 1. Checking the existence of the public SSH key file
def check_ssh_public_key(ssh_public_key_path):
    """Reading the content of the public SSH key file."""
    try:
        with open(ssh_public_key_path, 'r') as key_file:
            ssh_key = key_file.read().strip()
            return ssh_key
    except FileNotFoundError:
        print(f"Файл с ключом не найден: {ssh_public_key_path}")
        exit(1)

# Step 2. Data creation for terraform_meta.txt file
def create_terraform_meta_content(ssh_key):
    """Data creation for terraform_meta.txt file with public SSH key."""
    try:
        # Ask the user if they would like to keep the default data or modify it
        choice = input("Press enter to keep the default data (name, groups, shell, sudo), or type 'change' to modify it: ").strip().lower()

        if choice == 'change':
            # Requesting user values
            print("Empty input will keep the the default data: name (default: root), groups (default: sudo), shell (default: /bin/bash), sudo (default: 'ALL=(ALL) NOPASSWD:ALL')")
            name = input("Input value for 'name' (default: root): ") or "root"
            groups = input("Input value for 'groups' (default: sudo): ") or "sudo"
            shell = input("Input value for 'shell' (default: /bin/bash): ") or "/bin/bash"
            sudo = input("Input value for 'sudo' (default: 'ALL=(ALL) NOPASSWD:ALL'): ") or "ALL=(ALL) NOPASSWD:ALL"
        else:
            # Use default values
            name = "root"
            groups = "sudo"
            shell = "/bin/bash"
            sudo = "ALL=(ALL) NOPASSWD:ALL"

        terraform_meta_content = f"""#cloud-config
users:
  - name: {name}
    groups: {groups}
    shell: {shell}
    sudo: '{sudo}'
    ssh-authorized-keys:
      - {ssh_key}
"""
        return terraform_meta_content
    except Exception as e:
        print(f"An error occurred while generating the file content: {e}")
        exit(1)

if __name__ == "__main__":
    # Absolute paths to files and folders
    file_name = "terraform_meta.txt"
    meta_file_in_credentials = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{file_name}'
    meta_file_in_terraform = f'{env_var_dic["TERRAFORM_ABSOLUTE_PATH"]}/{file_name}'
    ssh_public_key_path = os.path.expanduser('~/.ssh/id_ed25519.pub')

    ssh_key = check_ssh_public_key(ssh_public_key_path) # Checking the existence of the public SSH key file
    terraform_meta_content = create_terraform_meta_content(ssh_key) # Generating data for writing to the file

    # Writing content to the "terraform_meta.txt " file
    write_txt_to_file(terraform_meta_content, meta_file_in_credentials) # For standardizing the storage of authentication variables
    write_txt_to_file(terraform_meta_content, meta_file_in_terraform) # For use with Terraform
