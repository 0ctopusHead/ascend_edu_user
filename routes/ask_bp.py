from flask import jsonify, Blueprint, request
from controller.AskController import AskController
from controller.FAQsController import FAQsController
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage, CarouselTemplate, CarouselColumn, TemplateSendMessage,
                            MessageAction)
from app import app, handler, line_bot_api
from flask import session

ask_bp = Blueprint('ask_bp', __name__)


@ask_bp.route("/callback", methods=['GET', 'POST'])
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
    try:
        query = event.message.text.lower()
        print(query)
        ask_controller = AskController()
        faqs_controller = FAQsController()
        if not query:
            return

        if query == "faqs":
            faqs = faqs_controller.get_faqs()
            if faqs:
                faqs_list = faqs[:5]
                columns = [
                    CarouselColumn(
                        title='FAQ',
                        text=faq["question"][:60],  # Truncate to avoid errors
                        actions=[MessageAction(label='See Answer', text=faq["question"])]
                    )
                    for faq in faqs_list
                ]

                carousel_template = CarouselTemplate(columns=columns)
                template_message = TemplateSendMessage(
                    alt_text='FAQs Carousel',
                    template=carousel_template
                )
            else:
                template_message = TextSendMessage(text="No FAQs are available at the moment.")
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

    except Exception as e:
        app.logger.error(f"Exception in handle_message: {e}")


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


@ask_bp.route('/projects/', methods=['GET'])
def projects():
    return 'The project page'
