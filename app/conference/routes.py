import datetime
from base64 import b64encode

from flask import Blueprint, Response, render_template

from app.conference import data, ical


# Google Calendar "From URL" subscription to /conferences.ics
GOOGLE_CALENDAR_ID = '4fqt0tj6gem0n2nulg8tkhkqqksi0733@import.calendar.google.com'

conference_handlers = Blueprint(
    'conference', __name__, template_folder='templates',
)


def google_calendar_src(calendar_id: str) -> str:
    return b64encode(calendar_id.encode()).decode().rstrip('=')


@conference_handlers.route('/conference')
def conference() -> str:
    today = datetime.date.today()
    conferences = [
        c for c in data.get_conferences().conferences if c.is_upcoming(today)
    ]
    return render_template(
        'conference.htm',
        conferences=conferences,
        today=today,
        last_updated=data.get_metadata().last_updated,
        calendar_src=google_calendar_src(GOOGLE_CALENDAR_ID),
    )


@conference_handlers.route('/conferences.ics')
def ical_file() -> Response:
    calendar = ical.generate_calendar(
        data.get_conferences().conferences,
        data.get_metadata().last_updated,
    )
    response = Response(calendar, mimetype='text/calendar')
    response.headers['Content-Disposition'] = 'attachment; filename=conferences.ics'
    return response
