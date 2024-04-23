import unittest
from main import app  

class TestSearchAPI(unittest.TestCase):
    def setUp(self):
        
        app.testing = True
        self.app = app.test_client()

    def test_valid_query(self):
        response = self.app.post('/search', json={'query': 'Roman Empire Greece'})
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



    def test_case_insensitivity(self):
        response1 = self.app.post('/search', json={'query': 'Ancient Greece'})
        response2 = self.app.post('/search', json={'query': 'ancient greece'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        data1 = response1.get_json()
        data2 = response2.get_json()
        self.assertEqual(data1['top_indices'], data2['top_indices'], "Search should be case insensitive")


    def test_partial_matches(self):
        response = self.app.post('/search', json={'query': 'Gree'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('top_indices', data)
        self.assertTrue(len(data['top_indices']) > 0, "Should return indices for partial matches if supported")



if __name__ == '__main__':
    unittest.main()
