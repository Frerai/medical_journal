from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate

def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(name=department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department
