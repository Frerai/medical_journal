from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from app.database.session import Base


# Create a Many-to-Many association table between admissions and doctors.
admission_doctor_association = Table(
    "admission_doctor_association", Base.metadata,
    Column("admission_id", Integer, ForeignKey("admissions.id")),
    Column("doctor_id", Integer, ForeignKey("doctors.id"))
)


class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    doctors = relationship("Doctor", secondary=admission_doctor_association, back_populates="admissions")

    patient = relationship("Patient", back_populates="admissions")
    department = relationship("Department", back_populates="admissions")
