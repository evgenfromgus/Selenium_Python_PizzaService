from pydantic import BaseModel, Field


class RegisterDataModel(BaseModel):
    # username: str = Field(..., min_length=1, max_length=100, pattern=r'^[A-Za-zА-Яа-я\s]+$')
    username: str = Field(
        ..., min_length=1, max_length=100, pattern=r"^[A-Za-zА-Яа-я0-9\s]+$"
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{1,}$",
    )
    password: str = Field(
        ..., min_length=1, max_length=20, pattern=r"^[A-Za-z0-9._@!#$%^&*()+=-]+$"
    )
