import os
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


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
    

def stop(msg: str):
    print(msg)
    exit()    


def chdir_parent(path):
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(path))))


def read_config(path):
    with open(path) as f:
        return yaml.safe_load(f.read())


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