from services.FAQsService import FAQsService
from flask import jsonify


class FAQsController:
    def __init__(self):
        self.faqs_service = FAQsService()

    def handle_user_query(self, query):
        try:
            query_doc = self.faqs_service.handle_user_query(query)
            return query_doc
        except Exception as e:
            return str(e), 400

    def compute_and_store_faqs(self):
        try:
            response_message, status_code = self.faqs_service.identify_potential_faqs()
            return response_message, status_code
        except ValueError as e:
            return str(e), 404

    def get_faqs(self):
        try:
            faqs = self.faqs_service.get_faqs()
            return faqs
        except Exception as e:
            return str(e), 404
