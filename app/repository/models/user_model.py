from dataclasses import dataclass

@dataclass
class UserModel:
    id: int
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
