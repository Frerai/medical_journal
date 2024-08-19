from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.models import doctor as doctor_model
from app.models import admission as admission_model
from app.schemas.doctor import Doctor
from app.schemas import patient as patient_schema
from app.schemas import doctor as doctor_schema
from app.api.crud import doctor as crud_doctor
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=doctor_schema.Doctor)
def create_doctor(doctor: doctor_schema.DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a new doctor with the provided details.

    Arguments:

        doctor: DoctorCreate - An object containing the details of the doctor to create.
        db: Session - A callable database object representing a transaction.

    Example:

        first_name: str = "Gregory"
        last_name: str = "House"
        department_id: int = 2

    Returns:

        The created doctor with their details.
    """
    db_doctor = crud_doctor.create_doctor(db, doctor)
    return db_doctor


@router.get("/", response_model=list[Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of doctors, with optional pagination.

    Arguments:

        skip: int - The number of doctors to skip (default is 0).
        limit: int - The maximum number of doctors to retrieve (default is 10).
        db: Session - A callable database object representing a transaction.

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of doctors, each containing their ID, name, and department.
    """
    doctors = crud_doctor.get_doctors(db, skip=skip, limit=limit)
    return doctors


@router.get("/{doctor_id}/patients", response_model=list[patient_schema.Patient])
def read_patients_for_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a list of patients associated with a specific doctor.

    Arguments:

        doctor_id: int - The unique identifier of the doctor whose patients are to be retrieved.
        db: Session - A callable database object representing a transaction.

    Example:

        doctor_id: int = 1

    Returns:

        A list of patients associated with the specified doctor.

    Raises:

        HTTPException: If the doctor with the specified ID does not exist.
    """
    patients = crud_doctor.get_patients_for_doctor(db, doctor_id=doctor_id)
    if not patients:
        raise HTTPException(status_code=404, detail="Doctor or Patients not found")
    return patients
