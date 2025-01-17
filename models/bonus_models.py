from pydantic import BaseModel, Field


class BonusDataModel(BaseModel):
    # имя: длина от 1 до 100 символов, любые буквы и пробелы
    name: str = Field(..., min_length=1, max_length=100, pattern=r"^[A-Za-zА-Яа-я\s]+$")
    # телефон: может начинаться с необязательного плюса, затем 10-12 цифр, допускаются пробелы и дефисы
    phone: str = Field(..., pattern=r"^\+?[\d\s\-]{10,15}$")
