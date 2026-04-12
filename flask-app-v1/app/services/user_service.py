from app.dto.user_dto import UserDto
from app.models.models import User
from app.extensions import db 

class UserService:

    def __init__(self, repo, mapper):
        self.repo = repo
        self.mapper = mapper
    
    def create_user(self, data):
        # user = User(**data)
        user = User(name=data["name"], email=data["email"])
        self.repo.add(user)
        dto = self.mapper.to_dto(user)
        return dto

    def get_all_users(self):
        users = self.repo.get_all()
        dtos: list[UserDto] = []
        for u in users:
            dto = self.mapper.to_dto(u)
            dtos.append(dto)
        return dtos
    
    # def get_user(self, user_id):
    #     return User.query.get(user_id)
    
    # def update_user(self, user_id, data):
    #     user = self.get_user(user_id)
    #     if not user:
    #         return None
    #     for key, value in data.items():
    #         setattr(user, key, value)
    #     db.session.commit()
    #     return user
    
    # def delete_user(self, user_id):
    #     user = self.get_user(user_id)
    #     if not user:
    #         return False
    #     db.session.delete(user)
    #     db.session.commit()
    #     return True