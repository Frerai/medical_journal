from pydantic import BaseModel
from pydantic import Field

class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, description="First name of the patient.")
    last_name: str = Field(..., min_length=1, description="Last name of the patient.")
    social_security_number: str = Field(
        ...,
        pattern=r"^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{2}-\d{4}$",
        description="Social security number of the patient."
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "first_name": "Albert",
                "last_name": "Einstein",
                "social_security_number": "140379-1234"
            }
        }

class Patient(PatientCreate):
    id: int

    class ConfigDict:
        from_attributes = True