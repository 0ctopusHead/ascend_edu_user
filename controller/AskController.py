from services.AskService import AskService


class AskController:
    def __init__(self):
        self.ask_service = AskService()
        pass

    def ask_endpoint(self, query):
        response_message, file_name = self.ask_service.ask(query)
        return response_message, file_name


