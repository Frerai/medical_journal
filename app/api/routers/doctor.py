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
    db_doctor = doctor_model.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.get("/", response_model=list[Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = crud_doctor.get_doctors(db, skip=skip, limit=limit)
    return doctors

@router.get("/{doctor_id}/patients", response_model=list[patient_schema.Patient])
def read_doctor_patients(doctor_id: int, db: Session = Depends(get_db)):
    patients = crud_doctor.get_patients_for_doctor(db, doctor_id=doctor_id)
    if not patients:
        raise HTTPException(status_code=404, detail="Doctor or Patients not found")
    return patients
