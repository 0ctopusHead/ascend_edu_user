from services.FAQsService import FAQsService
from flask import jsonify


class FAQsController:
    def __init__(self):
        self.faqs_service = FAQsService()

    def handle_user_query(self, query):
        query_doc = self.faqs_service.handle_user_query(query)
        return query_doc

    def compute_and_store_faqs(self):
        recent_queries = self.faqs_service.fetch_recent_queries()
        potential_faqs = self.faqs_service.identify_potential_faqs()
        self.faqs_service.store_faqs(potential_faqs)
        return potential_faqs
