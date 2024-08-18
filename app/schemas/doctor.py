from pydantic import BaseModel
from pydantic import Field

class DoctorCreate(BaseModel):
    first_name: str = Field(..., min_length=1, description="First name of the doctor.")
    last_name: str = Field(..., min_length=1, description="Last name of the patient.")
    department_name: str = Field(..., min_length=1, description="Name of department the doctor is a part of.")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "first_name": "Elmer",
                "last_name": "Hartman",
                "department_name": "Pediatrics"
            }
        }

class Doctor(DoctorCreate):
    id: int

    class ConfigDict:
        from_attributes = True
