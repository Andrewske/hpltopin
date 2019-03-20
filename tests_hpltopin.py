import unittest
import pinterest

class TestPinterest(unittest.TestCase):

    def test_get_access_token(self):
        result = pinterest.get_access_token(code)

