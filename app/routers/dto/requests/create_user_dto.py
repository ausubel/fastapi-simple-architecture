from pydantic import BaseModel, Field, validator
from datetime import date

class CreateUserDto(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email of the user")
    date_of_birth: date = Field(..., description="Date of birth of the user")
    
    @validator('date_of_birth')
    def ensure_18_or_over(cls, value):
        age = date.today().year - value.year
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return value
    
    @validator('email')
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError("Invalid email format")
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "jdoe@example.com",
                    "date_of_birth": "2000-01-01"
                }
            ]
        }
    }