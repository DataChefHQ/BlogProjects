import os


def get_relative_path(path: str) -> str:
    project_path = os.path.dirname(__file__)
    return os.path.join(project_path, path)