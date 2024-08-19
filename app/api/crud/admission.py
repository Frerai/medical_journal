from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.admission import Admission
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.admission import AdmissionCreate


def create_admission(db: Session, admission: AdmissionCreate):
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
    return db.query(Admission).filter(Admission.id == admission_id).first()

def get_admissions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Admission).offset(skip).limit(limit).all()