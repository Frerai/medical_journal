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
    patients = crud_patient.get_patients(db, skip=skip, limit=limit)
    return patients

@router.get("/{social_security_number}/doctors", response_model=list[Doctor])
def read_patient_doctors(social_security_number: str, db: Session = Depends(get_db)):
    doctors = crud_patient.get_doctors_for_patient(db, social_security_number=social_security_number)
    if not doctors:
        raise HTTPException(status_code=404, detail="Patient or Doctors not found")
    return doctors
