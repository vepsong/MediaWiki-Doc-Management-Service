import subprocess
import os
import re
import json
import yaml

# Retrieve the Git repository name and paths
def get_git_repo_info():
    """Retrieve the Git repository name and paths."""
    try:
        print("Running command to retrieve Git URL...")
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if result.returncode == 0:
            repo_url = result.stdout.strip()
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            print(f"Git repository name: {repo_name}")

            # Determining paths to the Git repository
            home_dir = os.path.expanduser("~")
            repo_relative_path = f"~/{repo_name}"  # Relative path to the Git repository, using '~'
            repo_path = os.path.join(home_dir, repo_name)  # Absolute path to the Git repository

            print(f"Relative path to the Git repository: {repo_relative_path}")
            print(f"Absolute path to the Git repository: {repo_path}")
            
            return repo_name, repo_relative_path, repo_path
        else:
            print("An error occurred while retrieving the Git repository URL")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Ask the user to input the Git repository name in case automatic retrieval fails
    while True:
        manual_repo_name = input("Failed to retrieve the repository name. Would you like to enter the Git repository name manually? (y/n): ").strip().lower()
        if manual_repo_name == 'y':
            repo_name = input("Input Git repository name: ").strip()
            if repo_name:
                print(f"Git repository name: {repo_name}")

                # Determining paths to the Git repository (after manual input)
                home_dir = os.path.expanduser("~")
                repo_relative_path = f"~/{repo_name}"  # Relative path to the Git repository, using '~' (after manual input)
                repo_path = os.path.join(home_dir, repo_name)  # Absolute path to the Git repository (after manual input)

                print(f"Relative path to the Git repository (after manual input): {repo_relative_path}")
                print(f"Absolute path to the Git repository (after manual input): {repo_path}")
                
                return repo_name, repo_relative_path, repo_path
            else:
                print("Git repository name cannot be empty. Please enter a valid name")
        elif manual_repo_name == 'n':
            print("Operation canceled. Git repository name was not provided.")
            return None, None, None
        else:
            print("Incorrect input. Please type 'y' (yes) or 'n' (no)")


# Universal function for searching a directory by pattern.
# For example, pattern='Ansible' or file_extension='.tf'.
    
def find_directory_by_pattern(repo_path=None, pattern=None, file_extension=None):
    """Universal function for searching a directory by pattern."""
    if not repo_path:
        print("Git repository name was not provided. Trying to retrieve it...")
        repo_name, repo_relative_path, repo_path = get_git_repo_info()
        if not repo_path:
            print("Failed to retrieve the Git repository name")
            return None, None, None
    
    # If a search template is provided (for example, 'ansible' or '.tf'), compile it into a regular expression
    if pattern:
        search_pattern = re.compile(pattern, re.IGNORECASE)
    
    # Iterating through all directories and files
    for root, dirs, files in os.walk(repo_path):
        # If the search template matches a folder name (for example, 'ansible')
        if pattern:
            for dir_name in dirs:
                if search_pattern.search(dir_name):
                    dir_relative_path = os.path.join(root, dir_name).replace(os.path.expanduser('~'), '~')
                    dir_absolute_path = os.path.abspath(os.path.join(root, dir_name)) 
                    print(f"Folder name based on the search template '{pattern}': {dir_name}")
                    print(f"Relative folder path: {dir_relative_path}")
                    print(f"Absolute folder path: {dir_absolute_path}")
                    return dir_name, dir_relative_path, dir_absolute_path
                
        # If the search template matches a file extension (for example, '.tf')
        if file_extension:
            for file in files:
                if file.endswith(file_extension):
                    folder_relative_path = root.replace(os.path.expanduser('~'), '~')
                    folder_absolute_path = os.path.abspath(root)
                    folder_name = os.path.basename(root)
                    print(f"Folder name based on the search template '{file_extension}': {folder_name}")
                    print(f"Relative folder path: {folder_relative_path}")
                    print(f"Absolute folder path: {folder_absolute_path}")
                    return folder_name, folder_relative_path, folder_absolute_path
    
    print(f"Folders, files based on the search template: '{pattern}' or file extensions based on the search template: '{file_extension}' were not found in the Git repository.") 

    return None, None, None


# Universal function for executing commands with result checking
def run_command(command, cwd=None, capture_output=False):
    """Universal function for executing commands with result checking."""
    try:
        result = subprocess.run(command, check=True, capture_output=capture_output, text=True, cwd=cwd)
        print(f"Command '{' '.join(command)}' was executed successfully.")
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during command execution: {e}")
        return e.returncode  # Returning an error code
    
# Universal function for writing data to a JSON file
def write_json_to_file(data, file_path):
    """Universal function for writing data to a JSON file."""
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"The file {file_path} was successfully created.")
    except (OSError, IOError) as e:
        print(f"An error occurred while writing data to the file {file_path}: {e}")

# Universal function for writing data to a txt file
def write_txt_to_file(data, file_path):
    """Universal function for writing data to a txt file."""
    try:
        with open(file_path, 'w') as txt_file:
            txt_file.write(data)
        print(f"The file {file_path} was successfully created.")
    except (OSError, IOError) as e:
        print(f"An error occurred while writing data to the file {file_path}: {e}")


# Universal function for writing data to a yaml file
def write_yaml_to_file(data, file_path, default_flow_style=False, indent=2):
    """Universal function for writing data to a yaml file."""
    try:
        with open(file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=default_flow_style, indent=indent, sort_keys=False, Dumper=yaml.SafeDumper)
        print(f"The file {file_path} was successfully created.")
    except (OSError, IOError) as e:
       print(f"An error occurred while writing data to the file {file_path}: {e}")


# Universal function for reading content from a JSON file
def load_json_data(file_path):
    """Universal function for reading content from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# Universal function to get the file path
def get_file_path(repo_name, folder_name, file_name):
    """Universal function to get the file path."""
    return os.path.expanduser(f'~/{repo_name}/{folder_name}/{file_name}')

# Universal function to add a variable to .bashrc file
def add_env_variable_to_bashrc(variable_name, value):
    """Universal function to add a variable to .bashrc file."""
    bashrc_path = os.path.expanduser('~/.bashrc')
    
    # Read the current contents of the .bashrc file
    with open(bashrc_path, 'r') as bashrc_file:
        lines = bashrc_file.readlines()

    # Checking for the existence of a variable and updating its value
    variable_found = False
    with open(bashrc_path, 'w') as bashrc_file:
        for line in lines:
            if line.startswith(f'export {variable_name}='):
                # The variable was found. Replacing it with a new value
                bashrc_file.write(f'export {variable_name}="{value}"\n')
                variable_found = True
                print(f"The environment variable {variable_name} was replaced {bashrc_path}.")
            else:
                bashrc_file.write(line)

        # If the environment variable was not found, add it to the end of the .bashrc file
        if not variable_found:
            bashrc_file.write(f'export {variable_name}="{value}"\n')
            print(f"The environment variable {variable_name} was added to {bashrc_path}.")


# Universal function to load and check environment variables in Python scripts

# Args:
# var_names (list): The list of names of the environment variables (e.g., env_vars = ["REPO_NAME", "REPO_PATH"])

# Returns:
# env_var_dic: A dictionary consisting of environment variable names and their values.

def load_and_check_env_vars(var_names):
    """Universal function to load and check environment variables in Python scripts."""
    # Load the environment variables into a dictionary
    env_var_dic = {var: os.environ.get(var) for var in var_names}
    
    # Check the values of the environment variables
    for var, value in env_var_dic.items():
        if value is None:
            print(f"The environment variable {var} is not set.")
        else:
            print(f"{var}: {value}")
    
    return env_var_dic


# Universal function to copy files from one directory to another directory
def copy_file(source_path, destination_path):
    """Universal function to copy files from one directory to another directory."""

    command = ['cp', source_path, destination_path]
    run_command(command)
