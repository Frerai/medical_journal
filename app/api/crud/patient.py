from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def get_patient_by_social_security_number(db: Session, social_security_number: str):
    return db.query(Patient).filter(Patient.social_security_number == social_security_number).first()


def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_doctors_for_patient(db: Session, social_security_number: str):
    patient = get_patient_by_social_security_number(db, social_security_number=social_security_number)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    doctors = []
    for admission in patient.admissions:
        doctors.extend(admission.doctors)

    return list(set(doctors))