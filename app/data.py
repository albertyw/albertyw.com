import json

import syspath

from app.util import cached_function


class Projects():
    def __init__(self) -> None:
        self.languages: list[Language] = []

    @staticmethod
    def load_from_file() -> 'Projects':
        current_directory = syspath.get_current_path()
        path = current_directory / 'data' / 'projects.json'
        with open(path, 'r') as handle:
            data = handle.read()
        parsed_data = json.loads(data)
        return Projects.load(parsed_data)

    @staticmethod
    def load(data: dict[str, dict[str, dict[str, str]]]) -> 'Projects':
        projects = Projects()
        for key, value in data.items():
            language = Language.load(key, value)
            projects.languages.append(language)
        return projects


class Language():
    def __init__(self) -> None:
        self.name: str = ''
        self.projects: list[Project] = []

    @staticmethod
    def load(key: str, data: dict[str, dict[str, str]]) -> 'Language':
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
    def load(key: str, data: dict[str, str]) -> 'Project':
        project = Project()
        project.name = key
        project.description = data.get('description', '')
        project.github = data.get('github', '')
        project.rubygems = data.get('rubygems', '')
        project.pypi = data.get('pypi', '')
        project.npm = data.get('npm', '')
        project.web = data.get('web', '')
        return project

    def links(self) -> dict[str, str]:
        links: dict[str, str] = {
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
        self.sections: list[Section] = []

    @staticmethod
    def load_from_file() -> 'Shelf':
        current_directory = syspath.get_current_path()
        path = current_directory / 'data' / 'shelf.json'
        with open(path, 'r') as handle:
            shelf_data = handle.read()
        parsed_data = json.loads(shelf_data)
        return Shelf.load(parsed_data)

    @staticmethod
    def load(shelf_data: dict[str, list[dict[str, str]]]) -> 'Shelf':
        shelf = Shelf()
        for key, value in shelf_data.items():
            section = Section.load(key, value)
            shelf.sections.append(section)
        return shelf


class Section():
    def __init__(self) -> None:
        self.name: str = ''
        self.items: list[Item] = []

    @staticmethod
    def load(name: str, data: list[dict[str, str]]) -> 'Section':
        section = Section()
        section.name = name
        for d in data:
            item = Item.load(d)
            section.items.append(item)
        return section


class Item():
    def __init__(self) -> None:
        self.name: str = ''
        self.link: str = ''

    @staticmethod
    def load(data: dict[str, str]) -> 'Item':
        item = Item()
        item.name = data['name']
        item.link = data['link']
        return item


@cached_function
def get_shelf() -> Shelf:
    loaded_shelf = Shelf.load_from_file()
    return loaded_shelf
