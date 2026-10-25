import json
import unittest

from app.conference import data


AGENTS_PATH = data.DIRECTORY / 'agents.json'
INSTRUCTIONS_PATH = data.DIRECTORY / 'INSTRUCTIONS.md'


class TestAgents(unittest.TestCase):
    def setUp(self) -> None:
        self.agents = json.loads(AGENTS_PATH.read_text())

    def test_researcher_is_read_only(self) -> None:
        researcher = self.agents['conference-researcher']
        self.assertEqual(researcher['tools'], ['WebSearch', 'WebFetch'])

    def test_researcher_model_is_pinned(self) -> None:
        researcher = self.agents['conference-researcher']
        self.assertEqual(researcher['model'], 'claude-haiku-5-5')

    def test_instructions_name_every_agent(self) -> None:
        instructions = INSTRUCTIONS_PATH.read_text()
        for name in self.agents:
            self.assertIn(f'`{name}`', instructions)
