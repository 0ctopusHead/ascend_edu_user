from flask import jsonify, Blueprint, request
from controller.AskController import AskController
ask_bp = Blueprint('ask_bp', __name__)


@ask_bp.route('/ask', methods=['POST'])
def ask_endpoint():
    data = request.get_json()
    query = data.get('query')
    ask_controller = AskController()
    response_message = ask_controller.ask_endpoint(query)
    return jsonify(
        {'response_message': response_message})