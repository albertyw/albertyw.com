import base64
import unittest
from unittest.mock import MagicMock, patch

from icalendar import Calendar

from app import serve
from app.conference import data, routes
from app.conference.tests.test_data import conference


CONFERENCES = data.Conferences.load({'conferences': [
    conference(id='past-2020', name='Past Conf 2020',
               start_date='2020-01-01', end_date='2020-01-02'),
    conference(cfp_deadline='2020-01-01'),
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
        self.assertIn(b'PyCon US 2027', page)
        self.assertIn(b'Early bird: 2027-03-01', page)
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

    def test_no_calendar_embed_without_id(self) -> None:
        self.assertNotIn(b'calendar.google.com', self.get('/conference'))

    @patch.object(routes, 'GOOGLE_CALENDAR_ID', 'abc@import.calendar.google.com')
    def test_calendar_embed(self) -> None:
        page = self.get('/conference')
        src = routes.google_calendar_src('abc@import.calendar.google.com')
        self.assertIn(b'calendar.google.com/calendar/embed', page)
        self.assertIn(src.encode(), page)

    def test_not_in_navbar(self) -> None:
        self.assertNotIn(b'href="/conference"', self.get('/'))

    def test_sitemap(self) -> None:
        self.assertIn(b'/conference<', self.get('/sitemap.xml'))


class TestGoogleCalendarSrc(unittest.TestCase):
    def test_google_calendar_src(self) -> None:
        # chase-center-calendar's embedded calendar
        calendar_id = 'i5nc55dcqfpnsptuej0ncldo4jgotqu0@import.calendar.google.com'
        src = routes.google_calendar_src(calendar_id)
        self.assertEqual(src, (
            'aTVuYzU1ZGNxZnBuc3B0dWVqMG5jbGRvNGpnb3RxdTBAaW1wb3J0'
            'LmNhbGVuZGFyLmdvb2dsZS5jb20'
        ))
        self.assertEqual(base64.b64decode(src + '=').decode(), calendar_id)


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
        self.assertIn('PyCon US 2027', summaries)
        self.assertNotIn('Undetermined Conf 2099', summaries)
