from app.dto.user_dto import UserDto
from app.models.user import User

class UserMapper:
    
    @staticmethod
    def to_dto(user: User) -> UserDto:
        return UserDto(id=user.id, name=user.name, email=user.email)
    
    