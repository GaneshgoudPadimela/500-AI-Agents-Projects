"""Tests for keyword_match.py (stdlib unittest, no extra dependencies).

Run from this folder:
    python -m unittest test_keyword_match -v
"""

import unittest

from keyword_match import find_keywords, keyword_match


class TestFindKeywords(unittest.TestCase):
    def test_finds_known_keywords_case_insensitively(self):
        found = find_keywords("Built services with JAVA, Spring Boot and Kafka.")
        self.assertIn("java", found)
        self.assertIn("spring boot", found)
        self.assertIn("kafka", found)

    def test_partial_words_do_not_count(self):
        # 'javascript' should not register as plain 'java'
        found = find_keywords("Frontend work in JavaScript only.")
        self.assertIn("javascript", found)
        self.assertNotIn("java", found)


class TestKeywordMatch(unittest.TestCase):
    def test_full_match_scores_100(self):
        result = keyword_match("Java and Kafka developer", "We need Java and Kafka.")
        self.assertEqual(result["score_percent"], 100.0)
        self.assertEqual(result["missing"], [])

    def test_missing_keywords_are_reported(self):
        result = keyword_match("Java developer", "We need Java, Kafka and Redis.")
        self.assertIn("kafka", result["missing"])
        self.assertIn("redis", result["missing"])
        self.assertIn("java", result["matched"])

    def test_empty_job_text_scores_zero(self):
        result = keyword_match("Java developer", "")
        self.assertEqual(result["score_percent"], 0.0)


if __name__ == "__main__":
    unittest.main()
