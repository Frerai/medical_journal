from pydantic import BaseModel
from pydantic import Field

class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Unique name for the department.")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "name": "Emergency Room"
            }
        }

class Department(DepartmentCreate):
    id: int

    class ConfigDict:
        from_attributes = True

