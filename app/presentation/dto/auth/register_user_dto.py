from pydantic import BaseModel, Field, field_validator
from datetime import date

class RegisterUserDto(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., min_length=6, description="Password of the user")
    date_of_birth: date = Field(..., description="Date of birth of the user")
    
    @field_validator('date_of_birth')
    def ensure_18_or_over(cls, value):
        age = date.today().year - value.year
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return value
    
    @field_validator('email')
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError("Invalid email format")
        return value
