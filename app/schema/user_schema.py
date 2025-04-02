from pydantic import BaseModel


# Create Pydantic models for response and request
class GetUserSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    name: str
    email: str


class UpdateUserSchema(BaseModel):
    name: str
    email: str
