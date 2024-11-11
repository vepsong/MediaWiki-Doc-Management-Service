import os
import re
from utils import load_and_check_env_vars  

# Importing environment variables into the script
env_vars = ["REPO_PATH"]

# Checking for the presence of environment variables and adding them to the dictionary
env_var_dic = load_and_check_env_vars(env_vars)

# Getting the list of all files in the directory
def get_file_names_in_directory(documentation_folder_path):
    """Getting the list of all files in the directory."""
    list_of_file_names = [
        file_name for file_name in os.listdir(documentation_folder_path)
        if os.path.isfile(os.path.join(documentation_folder_path, file_name))
    ]
    return list_of_file_names

# Adding indentation (tabulation) at the beginning of each line
def add_indentation(text, indent=None):
    """Adding indentation (tabulation) at the beginning of each line."""
    if indent is None:
        return text
    return '\n'.join(indent + line for line in text.splitlines())

# Updating the README.md file
def update_readme(content_files, readme_file, indent=None):
    """Updating the README.md file"""
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Iterating over all the files and inserting their content between the appropriate markers
    for content_file, start_marker, end_marker in content_files:
        # Opening the file to read content for insertion
        with open(content_file, 'r', encoding='utf-8') as f:
            new_content = f.read()

        # Adding indentation (tabulation) at the beginning of each line
        indented_content = add_indentation(new_content, indent)

        # Creating a template to search for content between appropriate markers
        pattern = re.compile(rf'{re.escape(start_marker)}.*?{re.escape(end_marker)}', re.DOTALL) 

        # Checking the existence of markers in the README.md file
        if not pattern.search(readme_content):
            print(f"Markers '{start_marker}' and/or '{end_marker}' were not found in {readme_file}. Skipping.")
            continue

        # Updating the content of the README.md file with added indentation (tabulation)
        readme_content = pattern.sub(f'{start_marker}\n{indented_content}\n{end_marker}', readme_content)

    # Saving the updated content to the README.md file
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"{readme_file} was successfully updated.")


if __name__ == "__main__":

    repo_dir = f'{env_var_dic["REPO_PATH"]}'

    documentation_folder_name = "project_documentation"
    documentation_folder_path = f'{repo_dir}/{documentation_folder_name}'

    readme_file_name = 'README.md'
    readme_file_path = f'{repo_dir}/{readme_file_name}'

    list_of_file_names = get_file_names_in_directory(documentation_folder_path)

    for name in list_of_file_names:
        content_files = [
            (f'{documentation_folder_path}/{name}', f'<!-- START_{name} -->', f'<!-- END_{name} -->'),
        ]

        # update_readme(content_files, readme_file_path, indent='\t')
        update_readme(content_files, readme_file_path, indent=None)
