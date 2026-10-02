import datetime
from typing import Any, Optional


def parse_date(value: Optional[str]) -> Optional[datetime.date]:
    if value is None:
        return None
    return datetime.date.fromisoformat(value)


class Deadline():
    def __init__(self) -> None:
        self.name: str = ''
        self.date: datetime.date = datetime.date.min

    @staticmethod
    def load(data: dict[str, str]) -> 'Deadline':
        deadline = Deadline()
        deadline.name = data['name']
        deadline.date = datetime.date.fromisoformat(data['date'])
        return deadline


class Conference():
    def __init__(self) -> None:
        self.id: str = ''
        self.name: str = ''
        self.start_date: Optional[datetime.date] = None
        self.end_date: Optional[datetime.date] = None
        self.location: Optional[str] = None
        self.website: str = ''
        self.registration_deadlines: list[Deadline] = []
        self.cfp_deadline: Optional[datetime.date] = None
        self.expected: str = ''
        self.source: str = ''
        self.last_verified: Optional[datetime.date] = None

    @staticmethod
    def load(data: dict[str, Any]) -> 'Conference':
        conference = Conference()
        conference.id = data['id']
        conference.name = data['name']
        conference.start_date = parse_date(data['start_date'])
        conference.end_date = parse_date(data['end_date'])
        conference.location = data['location']
        conference.website = data['website']
        conference.registration_deadlines = [
            Deadline.load(d) for d in data['registration_deadlines']
        ]
        conference.cfp_deadline = parse_date(data['cfp_deadline'])
        conference.expected = data.get('expected', '')
        conference.source = data['source']
        conference.last_verified = parse_date(data['last_verified'])
        conference.validate()
        return conference

    def validate(self) -> None:
        if (self.start_date is None) != (self.end_date is None):
            raise ValueError(f'{self.id}: set both start_date and end_date or neither')
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError(f'{self.id}: start_date is after end_date')
        if not self.website.startswith('https://'):
            raise ValueError(f'{self.id}: website must be https')

    @property
    def is_determined(self) -> bool:
        return bool(self.start_date and self.end_date and self.location)


class Conferences():
    def __init__(self) -> None:
        self.conferences: list[Conference] = []

    @staticmethod
    def load(data: dict[str, Any]) -> 'Conferences':
        conferences = Conferences()
        conferences.conferences = [Conference.load(c) for c in data['conferences']]
        ids = [c.id for c in conferences.conferences]
        if len(ids) != len(set(ids)):
            raise ValueError('conference ids must be unique')
        return conferences
