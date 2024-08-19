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
    return crud_admission.create_admission(db=db, admission=admission)

@router.get("/", response_model=list[Admission])
def read_admissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_admission.get_admissions(db=db, skip=skip, limit=limit)

@router.get("/{admission_id}", response_model=Admission)
def read_admission(admission_id: int, db: Session = Depends(get_db)):
    db_admission = crud_admission.get_admission(db, admission_id=admission_id)
    if not db_admission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admission not found")
    return db_admission
