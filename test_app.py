from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertIn('<table class="board"', html)
            self.assertEqual(response.status_code, 200)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            data = response.get_json()

            self.assertIsInstance(data["board"], list)
            self.assertIsInstance(data["gameId"], str)
            self.assertIn(data["gameId"], games)


    def test_api_score_word(self):
        """Test if word is valid, invalid, not-on-board"""

        with self.client as client:
            response = client.post('/api/new-game')
            data = response.get_json()

            gameId = data["gameId"]
            game = games[gameId]

            game.board = [
                ['A','Z','Z','Z','Z'],
                ['P','Z','Z','Z','Z'],
                ['P','Z','Z','Z','Z'],
                ['L','Z','Z','Z','Z'],
                ['E','Z','Z','Z','Z']]


            response = client.post('/api/score-word', json={'game_id': gameId, 'word': 'APPLE'})
            json_response = response.get_json()
            self.assertEqual({'result': 'ok'}, json_response)

            response = client.post('/api/score-word', json={'game_id': gameId, 'word': 'ZZZZZZZ'})
            json_response = response.get_json()
            self.assertEqual({'result': 'not-word'}, json_response)

            response = client.post('/api/score-word', json={'game_id': gameId, 'word': 'HELLO'})
            json_response = response.get_json()
            self.assertEqual({'result': 'not-on-board'}, json_response)
