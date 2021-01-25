import json
import os
from typing import Dict, List

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


class Shelf():
    def __init__(self) -> None:
        self.data: Dict[str, List[Dict[str, str]]]

    @staticmethod
    def load() -> 'Shelf':
        current_directory = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(current_directory, 'data', 'shelf.json')
        with open(path, 'r') as handle:
            shelf_data = handle.read()
        shelf = Shelf()
        shelf.data = json.loads(shelf_data)
        return shelf


@cached_function
def get_shelf() -> Shelf:
    loaded_shelf = Shelf.load()
    return loaded_shelf
