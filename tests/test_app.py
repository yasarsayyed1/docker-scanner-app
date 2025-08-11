import unittest
from src.app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter Docker image name', response.data)

    def test_scan_image(self):
        response = self.app.post('/scan', data={'image_name': 'nginx:latest'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Scan results for nginx:latest', response.data)

if __name__ == '__main__':
    unittest.main()