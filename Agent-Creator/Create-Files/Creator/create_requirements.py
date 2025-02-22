import os

def create_requirements(path):
    # pip install pipreqs
    # pipreqs /path/to/project
    before = os.getcwd()
    os.chdir(os.path.join(os.getcwd(), path))
    os.system(f"cd {path}")
    os.system("pip install pipreqs")
    os.system(f"pipreqs .")
    os.system("mv ../../requirements.txt .")
    os.chdir(before)
    return True
