import json
import os
from typing import Dict

from app.util import cached_function


class Projects():
    def __init__(self) -> None:
        self.data: Dict[str, Dict[str, Dict[str, str]]] = {}

    @staticmethod
    def load() -> 'Projects':
        current_directory = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(current_directory, 'data', 'projects.json')
        with open(path, 'r') as handle:
            project_data = handle.read()
        projects = Projects()
        projects.data = json.loads(project_data)
        return projects


@cached_function
def get_projects() -> Projects:
    loaded_projects = Projects.load()
    return loaded_projects
