import os
import shutil
import time

from jinja2 import Environment, FileSystemLoader


def stop(msg: str):
    print(msg)
    exit()


def contains_none(dic):
    for k, v in dic.items():
        if v is None:
            return True
        if isinstance(v, dict):
            if contains_none(v):
                return True
        if isinstance(v, list):
            for item in v:
                if contains_none(item):
                    return True
    return False


def handle_existing_file(file_path):
    if os.path.isfile(file_path):
        while True:
            user_choice = input(f"`{file_path}` already exists; (o)verwrite or (s)kip? ")
            if user_choice == 'o':
                backup(file_path)
                break
            elif user_choice == 's':
                break
            else:
                stop("Invalid input. Please enter 'o' to overwrite or 's' to skip.")


def mkdir_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)
        

def backup(path):
    ts = int(time.time())
    shutil.copy(path, f"{path}.{ts}.backup")


def expand_jinja_templates(base_dir, context):
    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(base_dir))

    # Recursively walk through the directory
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Check if the file has a .j2 extension
            if file.endswith(".j2"):
                # Remove the .j2 extension from the filename
                output_filename = file[:-3]

                # Create the output file path
                output_filepath = os.path.join(root, output_filename)

                # Render the Jinja template
                template_path = os.path.relpath(os.path.join(root, file), base_dir)
                template = env.get_template(template_path)
                rendered_content = template.render(context)

                # Write the rendered content to the output file
                with open(output_filepath, 'w') as output_file:
                    output_file.write(rendered_content)

                if output_filepath.endswith(".sh"):
                    os.chmod(output_filepath, 0o755)

                # Remove template file
                os.remove(os.path.join(root, file))