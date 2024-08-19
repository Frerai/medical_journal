from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of patients, with optional pagination.

    Arguments:

        db: Session - A callable database object representing a transaction.
        skip: int - The number of patients to skip (default is 0).
        limit: int - The maximum number of patients to retrieve (default is 10).

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of patients if found, otherwise an empty list.
    """
    return db.query(Patient).offset(skip).limit(limit).all()


def get_patient_by_social_security_number(db: Session, social_security_number: str):
    """
    Retrieve a patient by their social security number.

    Arguments:

        db: Session - A callable database object representing a transaction.
        social_security_number: str - The social security number of the patient to retrieve.

    Example:

        social_security_number: str = "140379-1234"

    Returns:

        The patient object if found, otherwise None.
    """
    return db.query(Patient).filter(Patient.social_security_number == social_security_number).first()


def create_patient(db: Session, patient: PatientCreate):
    """
    Create a new patient with the provided details.

    Arguments:

        db: Session - A callable database object representing a transaction.
        patient: PatientCreate - An object containing the details of the patient to create.

    Example:

        first_name: str = "Kenny"
        last_name: str = "McCormick"
        social_security_number: str = "220316-4321"

    Returns:

        The created patient object.
    """
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_doctors_for_patient(db: Session, social_security_number: str):
    """
    Retrieve a list of doctors associated with a specific patient.

    Arguments:

        db: Session - A callable database object representing a transaction.
        social_security_number: str - The unique identifier of the patient whose doctors are to be retrieved.

    Example:

        social_security_number: int = "111299-1234"

    Returns:

        A list of unique (no duplicates) doctor objects associated with the given patient if found,
        otherwise an empty list.
    """
    patient = get_patient_by_social_security_number(db, social_security_number=social_security_number)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    doctors = []
    for admission in patient.admissions:
        doctors.extend(admission.doctors)

    return list(set(doctors))