from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of doctors, with optional pagination.

    Arguments:

        db: Session - A callable database object representing a transaction.
        skip: int - The number of doctors to skip (default is 0).
        limit: int - The maximum number of doctors to retrieve (default is 10).

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of doctors if found, otherwise an empty list.
    """
    return db.query(Doctor).offset(skip).limit(limit).all()


def get_doctor_by_department(db: Session, department_name: str):
    return db.query(Doctor).filter(Doctor.department_name == department_name).first()


def create_doctor(db: Session, doctor: DoctorCreate):
    """
    Create a new doctor with the provided details.

    Arguments:

        db: Session - A callable database object representing a transaction.
        doctor: DoctorCreate - An object containing the details of the doctor to create.

    Example:

        first_name: str = "John Michael"
        last_name: str = "Dorian"
        department_id: int = 2

    Returns:

        The created doctor object.
    """
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_patients_for_doctor(db: Session, doctor_id: int):
    """
    Retrieve a list of patients assigned to a specific doctor.

    Arguments:

        db: Session - A callable database object representing a transaction.
        doctor_id: int - The unique identifier of the doctor whose patients are to be retrieved.

    Example:

        doctor_id: int = 1

    Returns:

        A list of patient objects associated with the given doctor.
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        patients = []
        for admission in doctor.admissions:
            patients.append(admission.patient)
        return patients
    return []