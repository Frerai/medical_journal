from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.api.crud import admission as crud_admission
from app.database.session import get_db
from app.schemas.admission import AdmissionCreate, Admission


router = APIRouter()

@router.post("/", response_model=Admission)
def create_admission(admission: AdmissionCreate, db: Session = Depends(get_db)):
    """
    Create a new admission with the provided details.

    Arguments:

        admission: AdmissionCreate - An object containing the details of the admission to create.
        db: Session - A callable database object representing a transaction.

    Example:

        department_id: int = 1
        patient_id: int = 2
        doctor_ids: list[int] = [1, 3]

    Returns:

        The created admission with its details.
    """
    return crud_admission.create_admission(db=db, admission=admission)


@router.get("/", response_model=list[Admission])
def read_admissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of admissions, with optional pagination.

    Arguments:

        skip: int - The number of admissions to skip (default is 0).
        limit: int - The maximum number of admissions to retrieve (default is 10).
        db: Session - A callable database object representing a transaction.

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of admissions, each containing their ID, department, patient, and doctors.
    """
    return crud_admission.get_admissions(db=db, skip=skip, limit=limit)


@router.get("/{admission_id}", response_model=Admission)
def read_admission(admission_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a specific admission by its ID.

    Arguments:

        admission_id: int - The unique identifier of the admission to retrieve.
        db: Session - A callable database object representing a transaction.

    Example:

        admission_id: int = 1

    Returns:

        The admission with the specified ID, including its department, patient, and doctors.

    Raises:

        HTTPException: If the admission with the specified ID does not exist.
    """
    db_admission = crud_admission.get_admission(db, admission_id=admission_id)
    if not db_admission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admission not found")
    return db_admission
