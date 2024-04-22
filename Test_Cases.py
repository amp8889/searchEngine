import unittest

from flask import app


class TestSearchAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_query(self):
        response = self.app.post('/search', json={'query': 'example search terms'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('top_indices', data)
        self.assertIsInstance(data['top_indices'], list)

    def test_missing_query_parameter(self):
        response = self.app.post('/search', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Query parameter missing in request')

    def test_empty_query_string(self):
        response = self.app.post('/search', json={'query': ''})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Query parameter missing in request')



if __name__ == '__main__':
    unittest.main()