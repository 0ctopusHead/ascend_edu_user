from flask import Blueprint, jsonify
from utils.extensions import timeloop
from datetime import timedelta
from app import app
faqs_bp = Blueprint('faqs_bp', __name__)
app = app


@timeloop.job(interval=timedelta(weeks=2))
def compute_and_store_faqs_tasks():
    from controller.FAQsController import FAQsController
    with app.app_context():
        print("FAQs have been computed")
        faqs_controller = FAQsController()
        response_message, status_code = faqs_controller.compute_and_store_faqs()
        return response_message, status_code


@faqs_bp.route('/compute_faqs/', methods=['POST'])
def trigger_compute_and_store_faqs():
    response_message, status_code = compute_and_store_faqs_tasks()
    return response_message, status_code


@faqs_bp.route('/get_faqs/', methods=['GET'])
def get_frequently_asked_question():
    from controller.FAQsController import FAQsController
    faqs_controller = FAQsController()
    faqs = faqs_controller.get_faqs()
    return faqs
