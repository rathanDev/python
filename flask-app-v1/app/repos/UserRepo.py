from app.models.user import User

class UserRepo:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return User.query.all()
    
    def get_by_id(self, user_id):
        return User.query.get(user_id)
    
    def add(self, user):
        self.db.session.add(user)
        self.db.session.commit()
        return user
    
    def delete(self, user):
        self.db.session.delete(user)
        self.db.session.commit()

