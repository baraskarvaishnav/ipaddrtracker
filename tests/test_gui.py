import unittest
from app.gui import IPTrackerApp
from tkinter import Tk

class TestIPTrackerApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = IPTrackerApp(self.root)

    def test_initialization(self):
        self.assertIsNotNone(self.app)

if __name__ == "__main__":
    unittest.main()

