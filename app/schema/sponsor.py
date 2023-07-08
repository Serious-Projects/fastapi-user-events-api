from pydantic import BaseModel, EmailStr, Field, validator


class SponsorCreate(BaseModel):
    name: str = Field(..., min_length=5, title="Name of the Sponsor")
    logo: str = Field(..., title="Logo/Brand of the Sponsor")
    contact: str

    @validator("contact")
    def validate_contact(cls, value):
        contact_number, email = value.split(" ")
        if not (
            contact_number.count("-") == 2
            and email.startswith("(")
            and email.endswith(")")
        ):
            raise ValueError("Invalid contact format")
        email = email[1:-1]
        email_str = EmailStr.validate(email)
        return f"{contact_number} ({email_str})"


class Sponsor(BaseModel):
    id: int
    name: str
    logo: str
    contact: str

    class Config:
        orm_mode = True
