import unittest
from app.utils import log_ip_history
import os

class TestUtils(unittest.TestCase):
    def test_log_ip_history(self):
        # Assuming data is a valid dict returned from the API
        data = {
            'query': '8.8.8.8',
            'country': 'United States',
            'regionName': 'California',
            'city': 'Mountain View',
            'zip': '94043',
            'lat': 37.386,
            'lon': -122.0838,
            'isp': 'Google LLC'
        }
        log_ip_history('8.8.8.8', data)
        self.assertTrue(os.path.exists('data/ip_history.csv'))

if __name__ == "__main__":
    unittest.main()

