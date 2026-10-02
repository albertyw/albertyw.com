import datetime
from base64 import b64encode

from flask import Blueprint, Response, render_template

from app.conference import data, ical


# Google Calendar "From URL" subscription to /conferences.ics; empty until set up
GOOGLE_CALENDAR_ID = ''

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
    calendar_src = ''
    if GOOGLE_CALENDAR_ID:
        calendar_src = google_calendar_src(GOOGLE_CALENDAR_ID)
    return render_template(
        'conference.htm',
        conferences=conferences,
        today=today,
        last_updated=data.get_metadata().last_updated,
        calendar_src=calendar_src,
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
