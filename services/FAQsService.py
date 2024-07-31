from app import mongo
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.preprocress import preprocess
from utils.BM25 import BM25
from collections import Counter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
db = mongo.db
ttl_duration = 14 * 24 * 60 * 60
db.queries_collection.create_index("date", expireAfterSeconds=ttl_duration)


class FAQsService:
    def __init__(self):
        self.database = db
        self.relevant_keywords = ["schedule", "syllabus", "regulation", "course", "exam", "grades", "lectures",
                                  "assignments", "examination"]
        self.tf_idf_vectorizer = TfidfVectorizer()
        self.bm25 = BM25(self.tf_idf_vectorizer)
        self.counter = Counter
        self.predefined_faqs = self.load_predefined_faqs()

    def load_predefined_faqs(self):
        predefined_faqs = [
            {"question": "What is the academic schedule for this semester?"},
            {"question": "When is the next final examination date?"},
            {"question": "When do classes start and end?"},
            {"question": "What are the important dates for this academic year?"},
            {"question": "Can I get the syllabus for 953331?"},
            {"question": "What topics are covered in 953331?"},
            {"question": "Who is the instructor for 953331?"},
            {"question": "What are the examination regulations?"},
            {"question": "Where can I find the academic regulations?"},
            {"question": "What is the grading policy?"}
        ]
        return predefined_faqs

    def is_query_relevant(self, query):
        query_tokens = preprocess(query)
        for token in query_tokens:
            if token in self.relevant_keywords:
                return True
        return False

    def handle_user_query(self, user_query):
        try:
            if self.is_query_relevant(user_query):
                processed_tokens = preprocess(user_query)
                query_doc = {
                    "text": user_query,
                    "date": datetime.datetime.utcnow(),
                    "processed_tokens": processed_tokens
                }
                self.database.queries_collection.insert_one(query_doc)
                self.find_relevant_faq(user_query)
                return query_doc
            else:
                raise ValueError("Query is not relevant to academic information")
        except Exception as e:
            raise e

    def fetch_recent_queries(self):
        two_weeks_ago = datetime.datetime.utcnow() - datetime.timedelta(weeks=2)
        recent_queries = list(self.database.queries_collection.find({"date": {"$gte": two_weeks_ago}}))
        return recent_queries

    def identify_potential_faqs(self, top_n=5):
        recent_queries = self.fetch_recent_queries()
        if not recent_queries:
            return []

        query_texts = [query['text'] for query in recent_queries]
        predefined_faqs = self.predefined_faqs
        faq_texts = [faq['question'] for faq in predefined_faqs]
        if not faq_texts:
            return []
        self.bm25.fit(faq_texts)
        scores = []
        for query in query_texts:
            score = self.bm25.transform(query)
            scores.append(score)
        average_scores = np.mean(scores, axis=0)
        print(average_scores)
        top_indices = np.argsort(average_scores)[-top_n:][::-1]
        potential_faqs = [faq_texts[i] for i in top_indices]

        return potential_faqs

    def find_relevant_faq(self, user_query):
        faq_texts = [faq['question'] for faq in self.predefined_faqs]

        if not faq_texts:
            return None

        faq_matrix = self.tf_idf_vectorizer.fit_transform(faq_texts)
        query_vector = self.tf_idf_vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vector, faq_matrix).flatten()
        most_similar_index = np.argmax(similarities)
        most_similar_score = similarities[most_similar_index]

        if most_similar_score >= 0.8:
            return self.predefined_faqs[most_similar_index]
        else:
            return None

    def store_faqs(self, potential_faqs):
        self.database.faqs_collection.delete_many({})
        for faq in potential_faqs:
            faq_doc = {
                "question": faq,
                "tokens": preprocess(faq)
            }
            self.database.faqs_collection.update_one({"question": faq}, {"$set": faq_doc}, upsert=True)
