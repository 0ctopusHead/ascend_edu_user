from flask import jsonify, Blueprint, request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    CarouselTemplate, CarouselColumn, TemplateSendMessage,
    MessageAction
)
from app import handler, line_bot_api
from controller.AuthenticationController import AuthenticationController
from controller.UserController import UserController
from controller.AskController import AskController
from controller.FAQsController import FAQsController

user_controller = UserController()
oauth_controller = AuthenticationController()
ask_bp = Blueprint('ask_bp', __name__)


@ask_bp.route("/callback", methods=['GET', 'POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    data = request.get_json()
    user_id = data.get('events', [{}])[0].get('source', {}).get('userId', '')
    print(user_id)

    access_token = oauth_controller.get_stored_token()

    if access_token and user_id:
        user_info = oauth_controller.get_user_info(access_token)
        cmu_account = user_info.get('cmuitaccount')
        user_controller.store_user(user_id, cmu_account)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature.", 400
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id

    user = user_controller.get_user(user_id)

    if not user or not user.get('cmu_account'):

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
            # Create a carousel of FAQ questions
            columns = [
                CarouselColumn(
                    title='FAQ',
                    text=faq["question"][:60],
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
        # For other queries, process the request and respond
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Processing your request...")
        )
        response_message = ask_controller.ask_endpoint(query)
        faqs_controller.handle_user_query(query)

        # Push the response message to the user
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=response_message)
        )



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
    return jsonify({'response_message': response_message})


@ask_bp.route('/login_callback', methods=['GET'])
def oauth_callback():
    # Handle OAuth callback to get the access token and user info
    response = oauth_controller.handle_oauth_callback()
    return response