import copy
import datetime
from typing import Any
import unittest

from app.conference import data


CONFERENCE: dict[str, Any] = {
    'cfp_deadline': '2026-12-19',
    'end_date': '2027-05-20',
    'id': 'pycon-us-2027',
    'last_verified': '2026-09-27',
    'location': 'Long Beach, CA, USA',
    'name': 'PyCon US 2027',
    'registration_deadlines': [{'date': '2027-03-01', 'name': 'Early bird'}],
    'source': 'https://us.pycon.org/2027/',
    'start_date': '2027-05-12',
    'website': 'https://us.pycon.org/2027/',
}


def conference(**overrides: Any) -> dict[str, Any]:
    conference_data = copy.deepcopy(CONFERENCE)
    conference_data.update(overrides)
    return conference_data


class TestConference(unittest.TestCase):
    def test_load(self) -> None:
        loaded = data.Conference.load(conference())
        self.assertEqual(loaded.id, 'pycon-us-2027')
        self.assertEqual(loaded.name, 'PyCon US 2027')
        self.assertEqual(loaded.start_date, datetime.date(2027, 5, 12))
        self.assertEqual(loaded.end_date, datetime.date(2027, 5, 20))
        self.assertEqual(loaded.location, 'Long Beach, CA, USA')
        self.assertEqual(loaded.website, 'https://us.pycon.org/2027/')
        self.assertEqual(loaded.cfp_deadline, datetime.date(2026, 12, 19))
        deadline = loaded.registration_deadlines[0]
        self.assertEqual(deadline.name, 'Early bird')
        self.assertEqual(deadline.date, datetime.date(2027, 3, 1))
        self.assertEqual(loaded.expected, '')
        self.assertEqual(loaded.last_verified, datetime.date(2026, 9, 27))
        self.assertTrue(loaded.is_determined)

    def test_load_undetermined(self) -> None:
        loaded = data.Conference.load(conference(
            start_date=None, end_date=None, location=None, cfp_deadline=None,
            last_verified=None, expected='May 2027',
        ))
        self.assertIsNone(loaded.start_date)
        self.assertIsNone(loaded.cfp_deadline)
        self.assertIsNone(loaded.last_verified)
        self.assertEqual(loaded.expected, 'May 2027')
        self.assertFalse(loaded.is_determined)

    def test_unknown_location_is_undetermined(self) -> None:
        loaded = data.Conference.load(conference(location=None))
        self.assertFalse(loaded.is_determined)

    def test_missing_key(self) -> None:
        conference_data = conference()
        del conference_data['cfp_deadline']
        with self.assertRaises(KeyError):
            data.Conference.load(conference_data)

    def test_invalid_date(self) -> None:
        with self.assertRaises(ValueError):
            data.Conference.load(conference(start_date='2027-05'))

    def test_one_date_null(self) -> None:
        with self.assertRaises(ValueError):
            data.Conference.load(conference(end_date=None))

    def test_start_after_end(self) -> None:
        with self.assertRaises(ValueError):
            data.Conference.load(conference(start_date='2027-05-21'))

    def test_website_not_https(self) -> None:
        with self.assertRaises(ValueError):
            data.Conference.load(conference(website='http://us.pycon.org/2027/'))


class TestConferences(unittest.TestCase):
    def test_load(self) -> None:
        conferences = data.Conferences.load(
            {'conferences': [conference()], 'rejected': []},
        )
        self.assertEqual(len(conferences.conferences), 1)

    def test_duplicate_ids(self) -> None:
        with self.assertRaises(ValueError):
            data.Conferences.load({'conferences': [conference(), conference()]})
