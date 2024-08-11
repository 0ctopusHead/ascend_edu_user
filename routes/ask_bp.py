from flask import jsonify, Blueprint, request
from controller.AskController import AskController
from controller.FAQsController import FAQsController

ask_bp = Blueprint('ask_bp', __name__)


@ask_bp.route('/ask/', methods=['POST'])
def ask_endpoint():
    data = request.get_json()
    query = data.get('query')
    ask_controller = AskController()
    faqs_controller = FAQsController()
    response_message = ask_controller.ask_endpoint(query)
    faqs_controller.handle_user_query(query)

    return jsonify(

        {'response_message': response_message})


@ask_bp.route('/projects/')
def projects():
    return 'The project page'
