import os
import shutil
import time
import yaml

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def stop(msg: str):
    print(msg)
    exit()


def contains_none(obj):
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
    

def read_cfg(path, join_with = None):
    try:
        with open(path) as f:
            return yaml.safe_load(f.read())
    except FileNotFoundError:
        stop(f"{path} not found. Did you forget to create it from the provided template?")


def mkdir_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)
        

def expand_jinja_templates(base_dir, context):
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