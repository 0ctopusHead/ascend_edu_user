
from flask import jsonify, Blueprint, request, session
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage, CarouselTemplate, CarouselColumn, TemplateSendMessage,
                            MessageAction)
from app import app, handler, line_bot_api
from controller.AuthenticationController import AuthenticationController
from controller.AskController import AskController
from controller.FAQsController import FAQsController
oauth_controller =AuthenticationController()
ask_bp = Blueprint('ask_bp', __name__)

@ask_bp.route("/callback", methods=['GET', 'POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature.", 400
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    access_token = oauth_controller.get_stored_token()
    print(access_token)
    if not access_token:
        login_url = "https://liff.line.me/2006144512-K614gPdV"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Please authenticate first by clicking the link: {login_url}")
        )
        return
    query = event.message.text.lower()
    ask_controller = AskController()
    faqs_controller = FAQsController()

    if not query:
        return

    if query == "faqs":
        faqs = faqs_controller.get_faqs()
        if isinstance(faqs, list) and faqs:
            columns = [
                CarouselColumn(
                    title='FAQ',
                    text=faq["question"][:60],  # Limiting the text to 60 characters
                    actions=[MessageAction(label='See Answer', text=faq["question"])]
                )
                for faq in faqs
            ]
            carousel_template = CarouselTemplate(columns=columns)
            template_message = TemplateSendMessage(
                alt_text='FAQs Carousel',
                template=carousel_template
            )
        else:
            error_message = faqs if isinstance(faqs, str) else "No FAQs are available at the moment."
            template_message = TextSendMessage(text=error_message)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Processing your request...")
        )
        response_message = ask_controller.ask_endpoint(query)
        faqs_controller.handle_user_query(query)

        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=response_message)
        )

@ask_bp.route('/login_callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')

    if not code:
        return jsonify({'error': 'Authorization code not provided.'}), 400

    access_token = oauth_controller.get_access_token(code)

    if not access_token:
        return jsonify({'error': 'Failed to obtain access token.'}), 400

    session['access_token'] = access_token

    user_info = oauth_controller.get_user_info(access_token)

    if user_info is None:
        return jsonify({'error': 'Failed to retrieve user information.'}), 400

    return jsonify(user_info)

def check_authorized():
    access_token = session.get('access_token')
    print(access_token)
    return access_token is not None

@ask_bp.route('/ask/', methods=['POST'])
def ask_endpoint():
    from controller.AskController import AskController
    from controller.FAQsController import FAQsController
    data = request.get_json()
    query = data.get('query')
    ask_controller = AskController()
    faqs_controller = FAQsController()
    response_message = ask_controller.ask_endpoint(query)
    faqs_controller.handle_user_query(query)
    return jsonify(
        {'response_message': response_message})


@ask_bp.route('/projects/', methods=['GET'])
def projects():
    return 'The project page'


@ask_bp.route('/test', methods=['GET'])
def test():
    access_token = session.get('access_token')
    print(access_token)
    return access_token