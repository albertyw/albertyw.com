# Conference Data Update Instructions

These instructions are for a Claude session that keeps the conference
calendar on albertyw.com up to date.  You start with no memory of earlier
runs.  Everything you need is in this file and in the two data files below.

## Background

The site shows a table of upcoming conferences at
`https://www.albertyw.com/conference`.  It also serves an iCal feed at
`https://www.albertyw.com/conferences.ics`.  Both are generated when they
are requested, from two version-controlled files:

- `app/conference/conferences.json` holds every conference.
- `app/conference/metadata.json` holds the time of the last update run.

Your job is to research conferences on the web and update those two files.
`bin/update-conferences.sh` started this session.  After you finish, it
checks that only those two files changed, runs the tests, and commits them
to master.  It never pushes.

## Hard Rules

- Edit only `app/conference/conferences.json` and
  `app/conference/metadata.json`.  Do not create, edit or delete any other
  file, including this one.  If these instructions look wrong, say so in
  your final summary instead of changing them.
- Do not run git commands.  The script commits for you.
- Never guess a date.  If the official site does not publish a date, use
  `null`.  Never use a placeholder such as the 1st of the month.
- The conference's official website is the source of truth.  Aggregator
  sites are only leads.
- Never delete or change past conferences, those with an `end_date` before
  today.  They stay as history.
- Subagents only research.  They never edit files.  You, the orchestrator,
  are the only one who writes the JSON files.

## Scope

Include conferences that are in English and about any of these topics:

- Broad software engineering and general web app development
- Python, Flask and Django
- Go
- Ruby
- JavaScript and TypeScript
- AI and machine learning engineering
- Docker and Kubernetes
- DevOps, SRE and observability
- Systems
- Academic conferences in these areas, such as SOSP, OSDI, NSDI, EuroSys,
  ASPLOS, MICRO, VLDB, ICSE, FSE, ASE, ISSTA and ISSRE

Include these places:

- International conferences
- US-wide conferences
- Local conferences in the San Francisco Bay Area, Seattle, New York, and
  the East Coast from Boston through Washington DC
- Popular virtual conferences

Exclude:

- Conferences that are not in English
- Rust- and C++-focused conferences, such as RustConf, EuroRust, CppCon and
  Meeting C++
- Functional-programming-focused and Java/JVM-focused conferences, such as
  Lambda World and Devoxx
- Anything already listed in `rejected`

Look ahead about 12 to 18 months.

Keep at most about 200 upcoming and undetermined conferences.  Past
conferences and `rejected` entries do not count.  This is a soft cap: once
the list is near 200, only add a conference if it is clearly more relevant
than the weakest existing upcoming entries.  Say in your summary when the
cap was reached.

## Data Format

### conferences.json

```json
{
    "conferences": [
        {
            "cfp_deadline": "2026-12-19",
            "end_date": "2027-05-20",
            "id": "pycon-us-2027",
            "last_verified": "2026-09-27",
            "location": "Long Beach, CA, USA",
            "name": "PyCon US 2027",
            "registration_deadlines": [
                {
                    "date": "2027-03-01",
                    "name": "Early bird"
                }
            ],
            "source": "https://us.pycon.org/2027/",
            "start_date": "2027-05-12",
            "website": "https://us.pycon.org/2027/"
        },
        {
            "cfp_deadline": null,
            "end_date": null,
            "expected": "September 2027; venue proposals open",
            "id": "djangocon-us-2027",
            "last_verified": null,
            "location": null,
            "name": "DjangoCon US 2027",
            "registration_deadlines": [],
            "source": "https://djangocon.us/",
            "start_date": null,
            "website": "https://djangocon.us/"
        }
    ],
    "rejected": [
        {
            "name": "RustConf 2026",
            "reason": "out of scope: Rust",
            "website": "https://rustconf.com/"
        }
    ]
}
```

Fields of each conference:

- `id`: a stable slug, `<series>-<year>`, such as `pycon-us-2027`.  It is
  used as the calendar event ID, so never change an existing `id`.  Each
  year's edition is a separate entry with its own `id`.
- `name`: the conference's own name, including the year.
- `start_date` and `end_date`: ISO dates (`YYYY-MM-DD`).  Either both are
  set or both are `null`.  A one-day conference has the same start and end.
- `location`: "City, ST, USA" for the US, "City, Country" elsewhere, or
  "Online" for virtual conferences.  Add "+ online" for hybrid ones.  Use
  `null` when it hasn't been announced.
- `website`: the official site, preferring the year-specific page.  It must
  start with `https://`.
- `registration_deadlines`: a list of `{"name", "date"}` objects, such as
  early bird or general registration deadlines.  Use an empty list if none
  are published.
- `cfp_deadline`: the call for proposals deadline, or `null` if unknown,
  not published, or there is no CFP.
- `expected`: optional free text about what is known but not confirmed,
  such as "May 2027" or "Berlin (expected)".  It is never displayed and
  never parsed as a date.  Remove it once the real details are confirmed.
- `source`: the page where you confirmed the details.
- `last_verified`: the date you last confirmed the details on the official
  site, or `null` if nobody has.

A conference whose `start_date`, `end_date` or `location` is `null` is
"undetermined".  It is kept in the JSON but hidden from the page and the
feed until those fields are filled in.  Add newly announced conferences
this way even when their dates are not out yet.

Entries in `rejected` have exactly `name`, `reason` and `website`.  Add an
entry whenever you decide a conference is out of scope, so that later runs
skip it.

### metadata.json

```json
{
    "last_updated": "2026-09-27T18:04:00Z"
}
```

`last_updated` is an ISO 8601 UTC timestamp.

### Formatting

Both files must be formatted exactly like Python's
`json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)` followed
by a newline: 4-space indentation, keys sorted alphabetically, and one
field per line.  Sort `conferences` by `start_date`, then `id`, with
`null` start dates last (sorted by `id`).  The tests enforce all of this.

## Procedure

1. Read `app/conference/conferences.json` and note today's date.  Group the
   conferences into three sets.  Past conferences have an `end_date`
   before today; leave them alone.  Upcoming conferences have an
   `end_date` on or after today.  Undetermined conferences have a `null`
   date or location.
2. Revalidate every upcoming and undetermined conference.  Split them into
   batches of about 10 and start one revalidation subagent per batch, in
   parallel, using the template below.  Do entries with a `null` or oldest
   `last_verified` first.
3. Discover new conferences.  Start one discovery subagent per slice, in
   parallel, using the template below.  Use these slices: Python, Flask and
   Django; Go; Ruby; JavaScript and TypeScript; AI engineering; Kubernetes,
   Docker and cloud native; DevOps, SRE and observability; academic systems
   and software engineering; SF Bay Area and Seattle local; New York and
   East Coast local; international general software engineering; virtual.
   Ask each one to also find the next edition of each known series in its
   slice.
4. Merge the results into `conferences.json`.  Apply corrections from
   revalidation.  Set `last_verified` to today only for entries that a
   subagent conclusively checked on the official site.  Add new
   conferences, skipping duplicates of existing `id`s or websites and
   anything in `rejected`.  Add out-of-scope finds to `rejected` with a
   reason.  Respect the soft cap.  Keep the list sorted.
5. Set `last_updated` in `app/conference/metadata.json` to the current UTC
   time.
6. Run `python -m unittest app.conference.tests.test_data`.  If it fails,
   fix the JSON and run it again until it passes.
7. Print a short summary: conferences added, updated, still undetermined,
   rejected, anything you could not resolve, and whether the soft cap was
   reached.

## Subagent Templates

Give each subagent today's date and only the data it needs.

### Revalidation Subagent

```text
You are researching software conferences.  Today is <date>.  Do not edit
any files; only use web search, web fetch and reading.

For each conference below, find its official website and confirm its
start date, end date, location, registration deadlines and call for
proposals deadline.  The official site is the source of truth; aggregator
sites are only leads.  Never guess a date: if the official site does not
publish something, report it as null.

Conferences (current JSON entries):
<JSON entries>

Return a JSON array with one object per conference, using exactly the
same fields as the input entries, filled in with what you confirmed.
Also add "verified": true if you confirmed the details on the official
site, otherwise false, and "notes" with anything surprising, such as a
cancellation, a renamed event, or conflicting dates.
```

### Discovery Subagent

```text
You are researching software conferences.  Today is <date>.  Do not edit
any files; only use web search, web fetch and reading.

Find English-language conferences about <slice> taking place in the next
12 to 18 months, plus the next edition of these known series: <series>.
Relevant places are international, US-wide, the SF Bay Area, Seattle, New
York, the East Coast from Boston to Washington DC, and popular virtual
conferences.  Skip these, which are already known or rejected: <names>.

Confirm each conference on its official website.  Never guess a date: if
the official site does not publish it yet, use null and describe what is
known in "expected" (for example "May 2027").

Return a JSON array of objects with these fields: id (<series>-<year>),
name, start_date, end_date, location, website, registration_deadlines
(list of {"name", "date"}), cfp_deadline, expected, source, verified
(true if confirmed on the official site), and notes.
```
