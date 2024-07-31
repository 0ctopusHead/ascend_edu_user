from services.AskService import AskService


class AskController:
    def __init__(self):
        self.ask_service = AskService()

    def ask_endpoint(self, query):
        response_message = self.ask_service.ask(query)
        print(response_message)
        return response_message


