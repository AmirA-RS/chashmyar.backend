from pydantic import BaseModel, Field
class token_data(BaseModel):
    username: str = Field(...)
    admin: bool = Field(...)

class token_show(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)
    class Config():
        orm_mode = True