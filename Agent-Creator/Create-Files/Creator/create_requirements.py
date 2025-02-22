import os


def create_requirements(path):
    # pip install pipreqs
    # pipreqs /path/to/project
    os.system(f"cd {path}")
    os.system("pip install pipreqs")
    os.system(f"pipreqs .")
    return True
