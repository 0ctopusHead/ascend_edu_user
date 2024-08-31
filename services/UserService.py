from app import mongo
from datetime import datetime
db = mongo.db
class UserService:
    def __init__(self):
        self.db = db

    def store_user_info(self, user_id, cmu_account):
        existing_user = self.db.users_collection.find_one({'user_id': user_id})
        account_conflict = self.db.users_collection.find_one({'cmu_account': cmu_account, 'user_id': {'$ne': user_id}})
        print(f"existing_user: {existing_user}")

        user_info = {
            'user_id': user_id,
            'cmu_account': cmu_account,
            'updated_at': datetime.utcnow()
        }
        print(f"user_info: {user_info}")
        if existing_user:
            self.db.users_collection.update_one(
                {'user_id': user_id},
                {'$set': user_info}
            )
            print("I'm in the existing_user IF cond")
            message = 'User information updated successfully'
        else:
            user_info['created_at'] = datetime.utcnow()
            self.db.users_collection.insert_one(user_info)
            message = 'New user information stored successfully'

        return {'message': message}

    def get_user_info(self, user_id):
        return self.db.users_collection.find_one({'user_id': user_id})