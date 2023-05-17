import os
import subprocess

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def contains_none(obj: dict):
    """
    Returns True if any value inside `obj` is a None.
    """

    if isinstance(obj, dict):
        for k, v in obj.items():
            if contains_none(v):
                return True
    elif isinstance(obj, list):
        for v in obj:
            if contains_none(v):
                return True
    else:
        return obj is None
    

def stop(msg: str):
    print(msg)
    exit()    


def chdir_parent(path):
    """
    Changes the working directory of the script to the parent directory 
    of the script. Since the scripts reside in a `do` directory, to avoid
    using "../" everywhere, we just cd to parent.
    """

    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(path))))


def read_config(path):
    with open(path) as f:
        return yaml.safe_load(f.read())


def expand_jinja_templates(base_dir, context):
    """
    Traverse a directory and expand all the found jinja templates. 
    After expansion, the templates will be deleted.
    :param base_dir: The directory to process.
    :param context: A dictionary containing the template parameters.
    """

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(base_dir), undefined=StrictUndefined)

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


def check_program_availability(program_name):
    print(f"Checking if {program_name} is installed")
    try:
        subprocess.run([program_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        stop(f'{program_name} is not installed. Please install it and start over.')


def check_successful_execution(command):
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False