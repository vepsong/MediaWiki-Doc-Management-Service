import os
from utils import load_and_check_env_vars, write_json_to_file

# Importing environment variables into the script
env_vars = ["REPO_PATH", "CREDENTIALS_DIR_ABSOLUTE_PATH", "TERRAFORM_ABSOLUTE_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)


# Step 1. Data creation for ansible_meta.json file
def create_ansible_meta_content():
    """Data creation for ansible_meta.json file."""
    try:
        # Ask the user if they would like to keep the default data or modify it
        print(f"Execution {file_name}")
        choice = input("Press enter to keep the default data (ansible_user, ansible_password, connection_protocol, ansible_become), or type 'change' to modify it: ").strip().lower()

        if choice == 'change':
            # Requesting user values
            print("Empty input will keep the the default data: 'ansible_user' (default: root), 'ansible_password' (default: ""), 'connection_protocol' (default: 'ssh')")
            ansible_user = input("Input value for 'ansible_user' (default: root): ") or "root"
            ansible_password = input("Input value for 'ansible_password' (default: ""): ") or ""
            connection_protocol = input("Input value for  'connection_protocol' (default: 'ssh'): ") or "ssh"
            
            # For ansible_become: accept only True/False and convert to a boolean value
            # while True:
            #     ansible_become_input = input("Input value for 'ansible_become' (True/False, default: False): ")
            #     if ansible_become_input.lower() in ["true", "false", ""]:
            #         ansible_become = ansible_become_input.lower() == "true" if ansible_become_input else False
            #         break
            #     else:
            #         print("Input error! Type 'True' или 'False'.")

        else:
            # Using default values
            ansible_user = "root"
            ansible_password = ""
            connection_protocol = "ssh"
            # ansible_become = False

        data = {
            "ansible_user": ansible_user,
            "ansible_password": ansible_password,
            "connection_protocol": connection_protocol,
            # "ansible_become": ansible_become
        }
        return data
    except Exception as e:
        print(f"An error occurred while generating the file content: {e}")
        exit(1)


if __name__ == "__main__":
    # Absolute paths to files and folders
    file_name = "ansible_meta.json"
    meta_file_in_credentials = f'{env_var_dic["CREDENTIALS_DIR_ABSOLUTE_PATH"]}/{file_name}'

    # Generating data for writing to the file
    ansible_meta_content = create_ansible_meta_content() 

    # Writing content to the "ansible_meta.json" file
    write_json_to_file(ansible_meta_content, meta_file_in_credentials) 
