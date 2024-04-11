import unittest
from score import get_score

TEST_STAMPS = [
    {"offset": 0, "score": {"home": 0, "away": 0}},
    {"offset": 2300, "score": {"home": 2, "away": 1}},
    {"offset": 23009, "score": {"home": 3, "away": 3}},
    {"offset": 30900, "score": {"home": 4, "away": 4}},
    {"offset": 40430, "score": {"home": 5, "away": 6}},
]


class TestScoreFunc(unittest.TestCase):
    def test_positive_cases(self):
        self.assertEqual(get_score(TEST_STAMPS, 0), (0, 0))
        self.assertEqual(get_score(TEST_STAMPS, 2300), (2, 1))
        self.assertEqual(get_score(TEST_STAMPS, 23009), (3, 3))
        self.assertEqual(get_score(TEST_STAMPS, 30900), (4, 4))
        self.assertEqual(get_score(TEST_STAMPS, 40430), (5, 6))

    def test_negative_cases(self):
        self.assertEqual(get_score(TEST_STAMPS, -50), (None, None))
        self.assertEqual(get_score(TEST_STAMPS, 3000), (None, None))
        self.assertEqual(get_score(TEST_STAMPS, 23010), (None, None))
        self.assertEqual(get_score(TEST_STAMPS, 30999), (None, None))
        self.assertEqual(get_score(TEST_STAMPS, 50111), (None, None))

if __name__ == '__main__':
    unittest.main()
