from app.repository.models.user_model import UserModel

class UserMapper:
    @staticmethod
    def to_model(row: tuple) -> UserModel:
        return UserModel(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            password=row[4],
            date_of_birth=row[5],
            role_id=row[6],
        )