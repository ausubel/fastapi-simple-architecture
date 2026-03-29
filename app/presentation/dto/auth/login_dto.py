from pydantic import BaseModel, Field, field_validator

class LoginDto(BaseModel):
    email: str = Field(..., description="Email string")
    password: str = Field(..., min_length=1, description="Password of the user")
    
    @field_validator('email')
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError("Invalid email format")
        return value

