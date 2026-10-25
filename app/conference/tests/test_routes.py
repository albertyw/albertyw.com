import unittest
from unittest.mock import MagicMock, patch

from icalendar import Calendar

from app import serve
from app.conference import data
from app.conference.tests.test_data import conference


CONFERENCES = data.Conferences.load({'conferences': [
    conference(id='past-2020', name='Past Conf 2020',
               start_date='2020-01-01', end_date='2020-01-02'),
    # Far-future dates so the page's real "today" never makes these past
    conference(id='future-2099', name='Future Conf 2099',
               start_date='2099-05-12', end_date='2099-05-20',
               cfp_deadline='2020-01-01',
               registration_deadlines=[{'date': '2099-03-01', 'name': 'Early bird'}]),
    conference(id='undetermined-2099', name='Undetermined Conf 2099',
               start_date=None, end_date=None, location=None),
]})


class TestConferencePage(unittest.TestCase):
    def setUp(self) -> None:
        serve.app.config['TESTING'] = True
        self.app = serve.app.test_client()

    def get(self, path: str) -> bytes:
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        page = response.get_data()
        response.close()
        return page

    def test_seed_data_page(self) -> None:
        page = self.get('/conference')
        self.assertIn(b'Conferences', page)
        self.assertIn(b'https://localhost/conferences.ics', page)
        self.assertIn(b'Last updated', page)

    @patch('app.conference.data.get_conferences')
    def test_shows_only_upcoming_determined(self, mock: MagicMock) -> None:
        mock.return_value = CONFERENCES
        page = self.get('/conference')
        self.assertIn(b'Future Conf 2099', page)
        self.assertIn(b'Early bird: 2099-03-01', page)
        self.assertNotIn(b'Past Conf 2020', page)
        self.assertNotIn(b'Undetermined Conf 2099', page)

    @patch('app.conference.data.get_conferences')
    def test_past_deadline_muted(self, mock: MagicMock) -> None:
        mock.return_value = CONFERENCES
        page = self.get('/conference').decode()
        self.assertRegex(page, r'text-muted">\s*2020-01-01')
        self.assertNotRegex(page, r'text-muted">\s*Early bird')

    @patch('app.conference.data.get_conferences')
    def test_no_conferences(self, mock: MagicMock) -> None:
        mock.return_value = data.Conferences()
        self.assertIn(b'No upcoming conferences', self.get('/conference'))

    def test_linked_from_reference(self) -> None:
        self.assertIn(b'href="/conference"', self.get('/reference'))

    def test_not_in_navbar(self) -> None:
        self.assertNotIn(b'href="/conference"', self.get('/'))

    def test_sitemap(self) -> None:
        self.assertIn(b'/conference<', self.get('/sitemap.xml'))


class TestICalFile(unittest.TestCase):
    def setUp(self) -> None:
        serve.app.config['TESTING'] = True
        self.app = serve.app.test_client()

    @patch('app.conference.data.get_conferences')
    def test_ical_file(self, mock: MagicMock) -> None:
        mock.return_value = CONFERENCES
        response = self.app.get('/conferences.ics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/calendar')
        self.assertIn('conferences.ics', response.headers['Content-Disposition'])
        events = list(Calendar.from_ical(response.get_data()).walk('VEVENT'))
        response.close()
        summaries = [str(e['summary']) for e in events]
        self.assertIn('Past Conf 2020', summaries)
        self.assertIn('Future Conf 2099', summaries)
        self.assertNotIn('Undetermined Conf 2099', summaries)
