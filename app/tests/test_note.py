import datetime
import json
import os
import re
import tempfile
import unittest

import pytz
import requests
from varsnap import TestVarSnap  # noqa: F401

from app import note_util


class TestNote(unittest.TestCase):
    def setUp(self):
        self.note = note_util.Note()

    def test_parse_time(self):
        time = 1504334092
        self.note.parse_time(time, pytz.timezone('America/Los_Angeles'))
        self.assertEqual(self.note.time.year, 2017)
        self.assertEqual(self.note.time.month, 9)
        self.assertEqual(self.note.time.day, 1)

    def test_parse_note(self):
        note = ['[x](y)']
        self.note.parse_note(note)
        self.assertEqual(self.note.note, '<p><a href="y">x</a></p>\n')


class UtilCase(unittest.TestCase):
    def test_get_malformed_note(self):
        note = b''
        note_file = tempfile.NamedTemporaryFile()
        note_file.write(note)
        note = note_util.get_note_file_data(note_file.name, None)
        self.assertEqual(note, None)
        note_file.close()

    def check_prune_note_files(self, file_name, assert_contains):
        note_files = note_util.prune_note_files([file_name])
        contains = file_name in note_files
        self.assertTrue(contains == assert_contains)

    def test_normal_notes(self):
        self.check_prune_note_files('asdf', True)

    def test_prune_tilde_notes(self):
        self.check_prune_note_files('asdf~', False)

    def test_prune_dotfile_notes(self):
        self.check_prune_note_files('.asdf', False)

    def test_get_note_from_unknown_slug(self):
        note = note_util.get_note_from_slug('asdf')
        self.assertEqual(note, None)

    def test_slug_lower_case(self):
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

    def check_grammar(self, text):
        text = re.sub(r"```[.\w\W]*```", "", text)
        text = re.sub(r"\[[.\w\W]*?\]\(.*?\)", "Z", text)
        text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)
        text = text.replace("`", "\"")
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
        response = requests.get(url, data, headers=headers)
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


def make_check_name(note):
    def test(self):
        self.check_grammar(note.markdown)
    return test


timezone = pytz.timezone(os.environ['DISPLAY_TIMEZONE'])
for note in note_util.get_notes():
    delta = datetime.datetime.now(tz=timezone) - note.time
    if delta > datetime.timedelta(days=30):
        continue
    test_func = make_check_name(note)
    setattr(TestGrammar, 'test_%s' % note.slug, test_func)
