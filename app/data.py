import json
import os
from typing import Dict, List

from app.util import cached_function


class Projects():
    def __init__(self) -> None:
        self.languages: List[Language] = []

    @staticmethod
    def load_from_file() -> 'Projects':
        current_directory = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(current_directory, 'data', 'projects.json')
        with open(path, 'r') as handle:
            data = handle.read()
        parsed_data = json.loads(data)
        return Projects.load(parsed_data)

    @staticmethod
    def load(data: Dict[str, Dict[str, Dict[str, str]]]) -> 'Projects':
        projects = Projects()
        for key, value in data.items():
            language = Language.load(key, value)
            projects.languages.append(language)
        return projects


class Language():
    def __init__(self) -> None:
        self.name: str = ''
        self.projects: List[Project] = []

    @staticmethod
    def load(key: str, data: Dict[str, Dict[str, str]]) -> 'Language':
        language = Language()
        language.name = key
        for key, value in data.items():
            project = Project.load(key, value)
            language.projects.append(project)
        return language


class Project():
    def __init__(self) -> None:
        self.name: str = ''
        self.description: str = ''
        self.github: str = ''
        self.rubygems: str = ''
        self.pypi: str = ''
        self.npm: str = ''
        self.web: str = ''

    @staticmethod
    def load(key: str, data: Dict[str, str]) -> 'Project':
        project = Project()
        project.name = key
        project.description = data.get('description', '')
        project.github = data.get('github', '')
        project.rubygems = data.get('rubygems', '')
        project.pypi = data.get('pypi', '')
        project.npm = data.get('npm', '')
        project.web = data.get('web', '')
        return project

    def links(self) -> Dict[str, str]:
        links: Dict[str, str] = {
            'github': self.github,
            'rubygems': self.rubygems,
            'pypi': self.pypi,
            'npm': self.npm,
            'web': self.web,
        }
        links = dict([(k, v) for k, v in links.items() if v])
        return links


@cached_function
def get_projects() -> Projects:
    loaded_projects = Projects.load_from_file()
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
