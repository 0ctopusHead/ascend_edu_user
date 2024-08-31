from services.UserService import UserService
class UserController:
    def __init__(self):
        self.user_service = UserService()

    def store_user(self, user_id, cmu_account):
        response_message = self.user_service.store_user_info(user_id, cmu_account)
        return response_message

    def get_user(self, user_id):
        return self.user_service.get_user_info(user_id)