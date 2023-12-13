import unittest
from utils import send_to_prometheus


class TestUtils(unittest.TestCase):
    def test_send_to_prometheus(self):
        send_to_prometheus({"a":['error_type'], "b":[]})


if __name__ == "__main__":
    unittest.main()
