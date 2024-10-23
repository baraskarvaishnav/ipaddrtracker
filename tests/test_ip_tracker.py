import unittest
from app.ip_tracker import track_ip

class TestIPTracker(unittest.TestCase):
    def test_track_ip(self):
        result = track_ip("8.8.8.8")  # Example IP (Google Public DNS)
        self.assertIsNotNone(result)
        self.assertEqual(result['query'], "8.8.8.8")

if __name__ == "__main__":
    unittest.main()

