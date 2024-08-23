import unittest
from unittest.mock import MagicMock, patch, ANY

from services.FAQsService import FAQsService

class TestGetFaqs(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_bm25 = MagicMock()
        self.faq_system = FAQsService()
        self.faq_system.database = self.mock_db


    def test_get_faqs_success(self):
        self.mock_db.faqs_collection.find.return_value = [
            {"question": "when is the next final examination date?"},
            {"question": "What are the examination regulations?"},
            {"question": "Where can I find the academic regulations?"},
            {"question": "What is the grading policy?"},
            {"question": "Who is the instructor for 953331?"}
        ]

        faqs = self.faq_system.get_faqs()
        expected_faqs = [
            {"question": "when is the next final examination date?"},
            {"question": "What are the examination regulations?"},
            {"question": "Where can I find the academic regulations?"},
            {"question": "What is the grading policy?"},
            {"question": "Who is the instructor for 953331?"}
        ]

        self.assertEqual(faqs, expected_faqs)


    def test_get_faqs_no_data(self):
        self.mock_db.faqs_collection.find.return_value = []
        with self.assertRaises(ValueError) as context:
            self.faq_system.get_faqs()
        self.assertEqual(str(context.exception), "No FAQs found in the database")


if __name__ == '__main__':
    unittest.main()