from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate

def get_department(db: Session, department_id: int):
    """
    Retrieve a department by its unique identifier.

    Arguments:

        db: Session - A callable database object representing a transaction.
        department_id: int - The unique identifier of the department to retrieve.

    Example:

        department_id: int = 1

    Returns:

        The department object if found, or None if the department does not exist.
    """
    return db.query(Department).filter(Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of departments with optional pagination.

    Arguments:

        db: Session - A callable database object representing a transaction.
        skip: int - The number of records to skip before starting to return results (default is 0).
        limit: int - The maximum number of records to return (default is 10).

    Example:

        skip: int = 0
        limit: int = 10

    Returns:

        A list of department objects within the specified range.
    """
    return db.query(Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: DepartmentCreate):
    """
    Create a new department in the database.

    Arguments:

        db: Session - A database session for executing queries.
        department: DepartmentCreate - The department data to be created.

    Returns:

        The newly created department record with an ID.
    """
    db_department = Department(name=department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department
