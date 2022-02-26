from pydantic import BaseModel, EmailError, EmailStr, Field
class token_data(BaseModel):
    email: EmailStr = Field(...)
    admin: bool = Field(...)

class token_show(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)
    class Config():
        orm_mode = True