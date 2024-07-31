from app import celery
from flask import Blueprint, jsonify
from controller.FAQsController import FAQsController

faqs_bp = Blueprint('faqs_bp', __name__)


@celery.task
def compute_and_store_faqs_tasks():
    faqs_controller = FAQsController()
    potential_faqs = faqs_controller.compute_and_store_faqs()
    return potential_faqs


@faqs_bp.route('/compute_faqs', methods=['POST'])
def trigger_compute_and_store_faqs():
    try:
        potential_faqs = compute_and_store_faqs_tasks()
        return jsonify({"faqs": potential_faqs}), 200
    except Exception as e:
        raise e

