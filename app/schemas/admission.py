from pydantic import BaseModel
from pydantic import Field

class AdmissionCreate(BaseModel):
    patient_id: int = Field(..., gt=0, description="ID of patient to be admitted.")
    department_id: int = Field(..., gt=0, description="ID of Department assigned to this admission.")
    doctor_ids: list[int] = Field(default=[], description="List of doctor(s) ID(s) assigned to this admission")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "patient_id": 1,
                "department_id": 4,
                "doctor_ids": [1, 2]
            }
        }

class Admission(AdmissionCreate):
    id: int

    class ConfigDict:
        from_attributes = True