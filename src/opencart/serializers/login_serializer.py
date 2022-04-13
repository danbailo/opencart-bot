from pydantic import BaseModel, Field


class LoginSerializer(BaseModel):
    user: str = Field(
        ..., alias='//input[@placeholder="Please enter username"]'
    )
    password: str = Field(
        ..., alias='//input[@placeholder="Please enter login password"]'
    )

    def return_alias_value(self, value: str):
        body = self.dict(by_alias=True)
        for key in body:
            if body[key] == value:
                return key

    class Config:
        allow_population_by_field_name = True
