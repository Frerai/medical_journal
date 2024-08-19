from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Doctor).offset(skip).limit(limit).all()

def get_doctor_by_department(db: Session, department_name: str):
    return db.query(Doctor).filter(Doctor.department_name == department_name).first()


def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_patients_for_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        patients = []
        for admission in doctor.admissions:
            patients.append(admission.patient)
        return patients
    return []