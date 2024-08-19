from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.models import patient as patient_model
from app.models import doctor as doctor_model
from app.models import admission as admission_model
from app.schemas import doctor as doctor_schema
from app.schemas.patient import Patient
from app.schemas.patient import PatientCreate
from app.schemas.doctor import Doctor
from app.database.session import get_db
from app.api.crud import patient as crud_patient

router = APIRouter()

@router.post("/", response_model=Patient)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new unique patient with the provided details.

    Arguments:

        patient: PatientCreate - An object containing the details of the patient to create.
        db: Session - A database session for executing queries.

    Example:

        first_name: str = "Albert"
        last_name: str = "Einstein"
        social_security_number: str = "140379-1234"

    Returns:

        The created patient with its details.
    """
    db_patient = crud_patient.get_patient_by_social_security_number(
        db,
        social_security_number=patient.social_security_number
    )
    if db_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this Social Security Number already registered"
        )
    return crud_patient.create_patient(db=db, patient=patient)


@router.get("/", response_model=list[Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of patients, with optional pagination.

    Arguments:

        skip: int - The number of patients to skip (default is 0).
        limit: int - The maximum number of patients to retrieve (default is 10).
        db: Session - A callable database object representing a transaction.

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of patients, each containing their ID, name, and social security number if found,
        otherwise an empty list.
    """
    patients = crud_patient.get_patients(db, skip=skip, limit=limit)
    return patients


@router.get("/{social_security_number}/doctors", response_model=list[Doctor])
def read_doctors_for_patient(social_security_number: str, db: Session = Depends(get_db)):
    """
    Retrieve a list of doctors associated with a specific patient.

    Arguments:

        social_security_number: str - The unique identifier of the patient whose doctors are to be retrieved.
        db: Session - A callable database object representing a transaction.

    Example:

        social_security_number: str = "170381-2234"

    Returns:

        A list of doctors associated with the specified patient.
    """
    doctors = crud_patient.get_doctors_for_patient(db, social_security_number=social_security_number)
    if not doctors:
        raise HTTPException(status_code=404, detail="Patient or Doctors not found")
    return doctors
