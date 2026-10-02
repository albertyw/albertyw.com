import datetime
from typing import NamedTuple, cast

from icalendar import Calendar, Event

from app.conference.data import Conference


UID_DOMAIN = 'albertyw.com'
SOURCE_OF_TRUTH = 'Website (source of truth - verify dates here)'


class Entry(NamedTuple):
    uid: str
    label: str
    start: datetime.date
    end: datetime.date


def entries(conference: Conference) -> list[Entry]:
    assert conference.start_date and conference.end_date
    conference_entries = [Entry(
        f'{conference.id}-conference@{UID_DOMAIN}', 'Conference',
        conference.start_date, conference.end_date,
    )]
    if conference.cfp_deadline:
        conference_entries.append(Entry(
            f'{conference.id}-cfp@{UID_DOMAIN}', 'Call for proposals deadline',
            conference.cfp_deadline, conference.cfp_deadline,
        ))
    for i, deadline in enumerate(conference.registration_deadlines):
        conference_entries.append(Entry(
            f'{conference.id}-registration-{i}@{UID_DOMAIN}',
            f'Registration deadline ({deadline.name})',
            deadline.date, deadline.date,
        ))
    return conference_entries


def summary(conference: Conference, entry: Entry) -> str:
    if entry.label == 'Conference':
        return conference.name
    return f'{entry.label}: {conference.name}'


def date_range(entry: Entry) -> str:
    if entry.start == entry.end:
        return entry.start.isoformat()
    return f'{entry.start.isoformat()} to {entry.end.isoformat()}'


def description(conference: Conference, current: Entry) -> str:
    conference_entries = entries(conference)
    width = max(len(e.label) for e in conference_entries) + 1
    lines = [
        summary(conference, current),
        '',
        f'{conference.name} - {conference.location}',
    ]
    for entry in conference_entries:
        marker = '>' if entry == current else ' '
        label = f'{entry.label}:'.ljust(width)
        lines.append(f'{marker} {label} {date_range(entry)}')
    lines += ['', f'{SOURCE_OF_TRUTH}: {conference.website}']
    return '\n'.join(lines)


def generate_event(
    conference: Conference, entry: Entry, modified: datetime.datetime,
) -> Event:
    event = Event()
    event.add('uid', entry.uid)
    event.add('summary', summary(conference, entry))
    event.add('dtstart', entry.start)
    event.add('dtend', entry.end + datetime.timedelta(days=1))
    event.add('location', conference.location)
    event.add('url', conference.website)
    event.add('description', description(conference, entry))
    event.add('dtstamp', modified)
    event.add('last-modified', modified)
    event.add('sequence', int(modified.timestamp()))
    return event


def generate_calendar(
    conferences: list[Conference], modified: datetime.datetime,
) -> bytes:
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//albertyw.com//Conferences//EN')
    cal.add('x-wr-calname', 'Conferences')
    cal.add('x-wr-caldesc', 'Software engineering conferences and deadlines')
    cal.add('x-published-ttl', 'PT1H')
    for conference in conferences:
        if not conference.is_determined:
            continue
        for entry in entries(conference):
            cal.add_component(generate_event(conference, entry, modified))
    return cast(bytes, cal.to_ical())
