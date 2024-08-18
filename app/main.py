from fastapi import FastAPI
from app.api.routers import admission
from app.api.routers import doctor
from app.api.routers import patient

from app.database.session import Base
from app.database.session import engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Journal")

app.include_router(admission.router, prefix="/admissions", tags=["admission"])
app.include_router(doctor.router, prefix="/doctors", tags=["doctor"])
app.include_router(patient.router, prefix="/patients", tags=["patient"])

@app.get("/")
def read_root():
    """
    Root endpoint to verify the service is running.

    Returns:
        dict: A welcome message.

    Example:

        {"message": "Welcome to the Medical Journal Patient Service"}
    """
    return {"message": "Welcome to the Medical Journal Patient Service"}
