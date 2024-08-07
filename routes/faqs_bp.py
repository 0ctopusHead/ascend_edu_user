from flask import Blueprint, jsonify
from controller.FAQsController import FAQsController
from utils.extensions import timeloop
from datetime import timedelta
faqs_bp = Blueprint('faqs_bp', __name__)


@timeloop.job(interval=timedelta(weeks=2))
def compute_and_store_faqs_tasks():
    print("FAQs have been computed")
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

