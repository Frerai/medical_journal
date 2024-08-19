from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.admission import Admission
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.admission import AdmissionCreate


def create_admission(db: Session, admission: AdmissionCreate):
    """
    Create a new admission with the provided details.

    Arguments:

        db: Session - A callable database object representing a transaction.
        admission: AdmissionCreate - An object containing the details of the admission to create.

    Example:

        department_id: int = 1
        patient_id: int = 2
        doctor_ids: list[int] = [1, 3] (default is [])

    Returns:

        The created admission object.

    Raises:

        HTTPException: If the provided patient ID does not exist.
        HTTPException: If the provided department ID does not exist.
        HTTPException: If the provided doctor(s) ID(s) does not exist.
    """
    # Lookup patient.
    patient = db.query(Patient).filter(Patient.id == admission.patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Lookup department.
    department = db.query(Department).filter(Department.id == admission.department_id).first()

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    # Create an admission.
    new_admission = Admission(patient_id=patient.id, department_id=department.id)

    # Add doctor(s).
    if admission.doctor_ids:
        doctors = db.query(Doctor).filter(Doctor.id.in_(admission.doctor_ids)).all()
        if len(doctors) != len(admission.doctor_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more doctors not found")
        new_admission.doctors = doctors

    db.add(new_admission)
    db.commit()
    db.refresh(new_admission)

    return new_admission

def get_admission(db: Session, admission_id: int):
    """
    Retrieve an admission by its ID.

    Arguments:

        db: Session - A callable database object representing a transaction.
        admission_id: int - The unique identifier of the admission to retrieve.

    Example:

        admission_id: int = 1

    Returns:

        The admission object if found, otherwise None.
    """
    return db.query(Admission).filter(Admission.id == admission_id).first()


def get_admissions(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of admissions, with optional pagination.

    Arguments:

        db: Session - A callable database object representing a transaction.
        skip: int - The number of admissions to skip (default is 0).
        limit: int - The maximum number of admissions to retrieve (default is 10).

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of admissions if found, otherwise an empty list.
    """
    return db.query(Admission).offset(skip).limit(limit).all()