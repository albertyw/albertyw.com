import datetime

from flask import Blueprint, Response, render_template

from app.conference import data, ical


conference_handlers = Blueprint(
    'conference', __name__, template_folder='templates',
)


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
