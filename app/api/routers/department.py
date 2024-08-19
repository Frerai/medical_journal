from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.api.crud import department as crud_department
from app.schemas.department import Department
from app.schemas.department import DepartmentCreate
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=Department)
def create_new_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    """
    Create a new department with a unique name.

    Arguments:

        department: DepartmentCreate - An object containing the name of the department to create.
        db: Session - A callable database object representing a transaction.

    Example:

        name: str = "Emergency Room"

    Returns:

        The created department with its ID and name.
    """
    db_department = crud_department.create_department(db=db, department=department)
    return db_department


@router.get("/", response_model=list[Department])
def read_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of departments, with optional pagination.

    Arguments:

        skip: int - The number of departments to skip (default is 0).
        limit: int - The maximum number of departments to retrieve (default is 10).
        db: Session - A callable database object representing a transaction.

    Returns:

        A list of departments, each containing its ID and name.
    """
    departments = crud_department.get_departments(db, skip=skip, limit=limit)
    return departments


@router.get("/{department_id}", response_model=Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a specific department by its ID.

    Arguments:

        department_id: int - The unique identifier of the department to retrieve.
        db: Session - A callable database object representing a transaction.

    Returns:

        The department with the specified ID, including its name.

    Raises:

        HTTPException: If the department with the specified ID does not exist.
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return db_department