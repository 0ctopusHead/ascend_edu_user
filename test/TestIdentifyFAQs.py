import unittest
from unittest.mock import MagicMock, patch, ANY
from bson import ObjectId
from services.FAQsService import FAQsService
import numpy as np

class TestIdentifyFAQs(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_bm25 = MagicMock()

        self.faq_system = FAQsService()
        self.faq_system.database = self.mock_db
        self.faq_system.bm25 = self.mock_bm25

        self.test_query = {
            "_id": ObjectId("64d8e9f3e47f9d3bcdcb32f4"),
            "text": "when is the next final examination date?",
            "processed_tokens": ["next", "final", "examination", "date"]
        }
        self.faq_system.predefined_faqs = [
            {"question": "When is the next final examination date?"},
            {"question": "How do I register for the next semester?"},
            {"question": "What is the tuition fee for the next semester?"}
        ]
        self.mock_db.queries_collection.find.return_value = [self.test_query]
        self.mock_bm25.transform.return_value = [0.9, 0.3, 0.1]

        self.mock_bm25.fit.return_value = None

    @patch("services.FAQsService.jsonify")
    def test_identify_potential_faqs(self, mock_jsonify):
        self.mock_bm25.transform.return_value = np.array([0.9, 0.3, 0.1])
        response, status_code = self.faq_system.identify_potential_faqs(top_n=1)

        expected_faq = "When is the next final examination date?"
        self.mock_db.faqs_collection.update_one.assert_called_with(
            {"question": expected_faq},
            {"$set": {
                "_id": ANY,
                "question": expected_faq,
                "date": ANY
            }},
            upsert=True
        )

        mock_jsonify.assert_called_with({"message": "Top 5 potential FAQs have been successfully identified and updated in the database."})
        self.assertEqual(status_code, 200)


    def test_identify_potential_faqs_no_queries(self):
        self.mock_db.queries_collection.find.return_value = []
        with self.assertRaises(ValueError) as context:
            self.faq_system.identify_potential_faqs()
        self.assertEqual(str(context.exception), "Could not find any queries from the last two weeks")

if __name__ == '__main__':
    unittest.main()
