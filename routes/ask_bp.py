from flask import jsonify, Blueprint, request
from controller.AskController import AskController
from controller.FAQsController import FAQsController
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,ButtonsTemplate,TemplateSendMessage,
                            MessageAction)
from app import app, handler, line_bot_api
ask_bp = Blueprint('ask_bp', __name__)


@ask_bp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        raise

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    query = event.message.text.lower()
    ask_controller = AskController()
    faqs_controller = FAQsController()

    if query == "faqs":
        faqs = faqs_controller.get_faqs()
        if faqs:
            buttons_template = ButtonsTemplate(
                title='FAQs',
                text='Please select a FAQ:',
                actions=[
                    MessageAction(label=faq["question"], text=faq["question"])
                    for faq in faqs["faqs"]
                ]
            )
            template_message = TemplateSendMessage(
                alt_text='FAQs',
                template=buttons_template
            )
        else:
            template_message = TextSendMessage(text="No FAQs are available at the moment.")

        line_bot_api.reply_message(event.reply_token, template_message)

    else:

        response_message = ask_controller.ask_endpoint(query)
        faqs_controller.handle_user_query(query)

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))
        return jsonify(
            {'response_message': response_message})

@ask_bp.route('/ask/', methods=['POST'])
def ask_endpoint(event):
    query = event.message.text
    ask_controller = AskController()
    faqs_controller = FAQsController()
    response_message = ask_controller.ask_endpoint(query)
    faqs_controller.handle_user_query(query)
    return jsonify(
        {'response_message': response_message})


@ask_bp.route('/projects/', methods=['GET'])
def projects():
    return 'The project page'
