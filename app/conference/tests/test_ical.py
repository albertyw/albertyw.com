import datetime
from typing import Any
import unittest

from icalendar import Calendar

from app.conference import data, ical
from app.conference.tests.test_data import conference


MODIFIED = datetime.datetime(2026, 9, 27, 18, 4, tzinfo=datetime.timezone.utc)


def load(**overrides: Any) -> data.Conference:
    return data.Conference.load(conference(**overrides))


def parse(calendar: bytes) -> list[Any]:
    return list(Calendar.from_ical(calendar).walk('VEVENT'))


class TestEntries(unittest.TestCase):
    def test_entries(self) -> None:
        entries = ical.entries(load())
        self.assertEqual([e.uid for e in entries], [
            'pycon-us-2027-conference@albertyw.com',
            'pycon-us-2027-cfp@albertyw.com',
            'pycon-us-2027-registration-0@albertyw.com',
        ])
        self.assertEqual(entries[0].start, datetime.date(2027, 5, 12))
        self.assertEqual(entries[0].end, datetime.date(2027, 5, 20))
        self.assertEqual(entries[1].start, datetime.date(2026, 12, 19))
        self.assertEqual(entries[2].label, 'Registration deadline (Early bird)')

    def test_entries_without_deadlines(self) -> None:
        entries = ical.entries(load(cfp_deadline=None, registration_deadlines=[]))
        self.assertEqual(len(entries), 1)

    def test_summary(self) -> None:
        conf = load()
        summaries = [ical.summary(conf, e) for e in ical.entries(conf)]
        self.assertEqual(summaries, [
            'PyCon US 2027',
            'Call for proposals deadline: PyCon US 2027',
            'Registration deadline (Early bird): PyCon US 2027',
        ])


class TestDescription(unittest.TestCase):
    def test_description(self) -> None:
        conf = load()
        entry = ical.entries(conf)[2]
        self.assertEqual(ical.description(conf, entry), '\n'.join([
            'Registration deadline (Early bird): PyCon US 2027',
            '',
            'PyCon US 2027 - Long Beach, CA, USA',
            '  Conference:                         2027-05-12 to 2027-05-20',
            '  Call for proposals deadline:        2026-12-19',
            '> Registration deadline (Early bird): 2027-03-01',
            '',
            'Website (source of truth - verify dates here): '
            'https://us.pycon.org/2027/',
        ]))

    def test_every_event_references_all_dates(self) -> None:
        conf = load()
        for entry in ical.entries(conf):
            text = ical.description(conf, entry)
            for date in ['2027-05-12', '2027-05-20', '2026-12-19', '2027-03-01']:
                self.assertIn(date, text)
            self.assertIn(conf.website, text)
            self.assertEqual(text.count('\n>'), 1)

    def test_single_day_conference(self) -> None:
        conf = load(end_date='2027-05-12')
        text = ical.description(conf, ical.entries(conf)[0])
        self.assertIn('> Conference:', text)
        self.assertNotIn(' to ', text)


class TestGenerateCalendar(unittest.TestCase):
    def test_calendar(self) -> None:
        calendar = Calendar.from_ical(ical.generate_calendar([load()], MODIFIED))
        self.assertEqual(calendar['x-wr-calname'], 'Conferences')
        events = list(calendar.walk('VEVENT'))
        self.assertEqual(len(events), 3)

    def test_all_day_events(self) -> None:
        events = parse(ical.generate_calendar([load()], MODIFIED))
        conf_event, cfp_event = events[0], events[1]
        self.assertEqual(conf_event['summary'], 'PyCon US 2027')
        self.assertEqual(conf_event.decoded('dtstart'), datetime.date(2027, 5, 12))
        self.assertEqual(conf_event.decoded('dtend'), datetime.date(2027, 5, 21))
        self.assertEqual(cfp_event.decoded('dtstart'), datetime.date(2026, 12, 19))
        self.assertEqual(cfp_event.decoded('dtend'), datetime.date(2026, 12, 20))
        self.assertEqual(cfp_event['location'], 'Long Beach, CA, USA')
        self.assertEqual(cfp_event['url'], 'https://us.pycon.org/2027/')
        self.assertEqual(cfp_event.decoded('dtstamp'), MODIFIED)

    def test_skips_undetermined(self) -> None:
        undetermined = load(
            id='djangocon-us-2027', start_date=None, end_date=None, location=None,
        )
        events = parse(ical.generate_calendar([undetermined, load()], MODIFIED))
        self.assertEqual(len(events), 3)
        self.assertTrue(all('pycon' in str(e['uid']) for e in events))

    def test_deterministic(self) -> None:
        conferences = [load()]
        self.assertEqual(
            ical.generate_calendar(conferences, MODIFIED),
            ical.generate_calendar(conferences, MODIFIED),
        )

    def test_seed_data(self) -> None:
        conferences = data.Conferences.load_from_file().conferences
        modified = data.Metadata.load_from_file().last_updated
        events = parse(ical.generate_calendar(conferences, modified))
        self.assertNotEqual(events, [])
