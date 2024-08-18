from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routers import admission
from app.api.routers import department
from app.api.routers import doctor
from app.api.routers import patient

from app.database.session import Base
from app.database.session import engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Journal")

app.include_router(admission.router, prefix="/admissions", tags=["admission"])
app.include_router(department.router, prefix="/departments", tags=["department"])
app.include_router(doctor.router, prefix="/doctors", tags=["doctor"])
app.include_router(patient.router, prefix="/patients", tags=["patient"])

# Ensure first page user will see, is the "/docs" endpoint for help.
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")