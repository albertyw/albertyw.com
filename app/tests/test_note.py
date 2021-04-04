import datetime
import json
import os
import re
import tempfile
import unittest

import pytz
import requests
from titlecase import titlecase
from typing import Any, Callable, cast
from varsnap import test

from app import note_util, serve


class TestNote(unittest.TestCase):
    def setUp(self) -> None:
        self.note = note_util.Note()

    def test_parse_time(self) -> None:
        time = 1504334092
        parsed_time = note_util.Note.parse_time(
            time,
            pytz.timezone('America/Los_Angeles')
        )
        self.assertEqual(parsed_time.year, 2017)
        self.assertEqual(parsed_time.month, 9)
        self.assertEqual(parsed_time.day, 1)

    def test_parse_markdown(self) -> None:
        markdown = '[x](y)'
        note = note_util.Note.parse_markdown(markdown)
        self.assertEqual(note, '<p><a href="y">x</a></p>\n')

    def test_get_malformed_note(self) -> None:
        note_data = b''
        with tempfile.NamedTemporaryFile() as note_file:
            note_file.write(note_data)
            note = note_util.Note.get_note_file_data(note_file.name, pytz.UTC)
            self.assertEqual(note, None)

    def test_write_note(self) -> None:
        with tempfile.NamedTemporaryFile() as note_file:
            self.note.note_file = note_file.name
            self.note.title = 'title'
            self.note.slug = 'slug'
            self.note.time = datetime.datetime.now()
            self.note.markdown = 'markdown'
            self.note.note = note_util.Note.parse_markdown(self.note.markdown)
            self.note.write_note()
            note_file.flush()
            with open(note_file.name, 'r') as handle:
                data = handle.read()
            self.assertIn('title', data)
            self.assertIn('slug', data)
            self.assertIn('markdown', data)


class UtilCase(unittest.TestCase):
    def check_prune_note_files(
        self,
        file_name: str,
        assert_contains: bool
    ) -> None:
        note_files = note_util.prune_note_files([file_name])
        contains = file_name in note_files
        self.assertTrue(contains == assert_contains)

    def test_normal_notes(self) -> None:
        self.check_prune_note_files('asdf', True)

    def test_prune_tilde_notes(self) -> None:
        self.check_prune_note_files('asdf~', False)

    def test_prune_dotfile_notes(self) -> None:
        self.check_prune_note_files('.asdf', False)

    def test_get_note_from_unknown_slug(self) -> None:
        note = note_util.get_note_from_slug('asdf')
        self.assertEqual(note, None)

    def test_slug_lower_case(self) -> None:
        notes = note_util.get_notes()
        for note in notes:
            self.assertEqual(note.slug, note.slug.lower())


class TestGrammar(unittest.TestCase):

    IGNORED = [
        'DASH_RULE',
        'EN_QUOTES',
        'MORFOLOGIK_RULE_EN_US',
        'NUMEROUS_DIFFERENT',
        'PUNCTUATION_PARAGRAPH_END',
        'SENTENCE_WHITESPACE',
        'SOME_OF_THE',
        'WHITESPACE_RULE',
        'METRIC_UNITS_EN_US',
    ]
    IGNORED_KEYWORDS = [
        'curriculum',
        'Use a comma before',
        '777',
    ]

    def check_grammar(self, text: str) -> None:
        text = re.sub(r"```[.\w\W]*```", "CODE", text)
        text = re.sub(r"`[.\w\W]*`", "CODE", text)
        text = re.sub(r"\[[.\w\W]*?\]\(.*?\)", "Z", text)
        text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)
        text = text.replace("\n", " ")
        url = 'http://api.grammarbot.io/v2/check'
        headers = {
            'content-type': 'application/json',
        }
        data = {
            'api_key': os.environ.get('GRAMMARBOT_TOKEN'),
            'language': 'en-US',
            'text': text,
        }
        response = requests.get(url, cast(Any, data), headers=headers)
        content = json.loads(response.content)
        matches = content['matches']
        matches = [
            m for m in matches
            if m['rule']['id'] not in TestGrammar.IGNORED
        ]
        matches = [
            m for m in matches
            if not any([
                i in m['message'] for i in TestGrammar.IGNORED_KEYWORDS
            ])
        ]
        self.assertEqual(len(matches), 0, json.dumps(matches, indent=4))


class TestStyle(unittest.TestCase):
    def check_title_case(self, note: note_util.Note) -> None:
        self.assertEqual(note.title, titlecase(note.title), note.note_file)


def make_check_grammar(note: note_util.Note) -> Callable[..., None]:
    def test(self: Any) -> None:
        self.check_grammar(note.markdown)
    return test


def make_check_style(note: note_util.Note) -> Callable[..., None]:
    def test(self: Any) -> None:
        self.check_title_case(note)
    return test


timezone = pytz.timezone(os.environ['DISPLAY_TIMEZONE'])
first = True
for note in note_util.get_notes():
    delta = datetime.datetime.now(tz=timezone) - note.time
    if delta <= datetime.timedelta(days=30) or first:
        test_func = make_check_grammar(note)
        setattr(TestGrammar, 'test_%s' % note.slug, test_func)
        first = False
    test_func = make_check_style(note)
    setattr(TestStyle, 'test_%s' % note.slug, test_func)


class TestIntegration(unittest.TestCase):
    def test_varsnap(self) -> None:
        with serve.app.test_request_context():
            matches, logs = test()
        if matches is None:
            raise unittest.case.SkipTest('No Snaps found')  # pragma: no cover
        self.assertTrue(matches, logs)
