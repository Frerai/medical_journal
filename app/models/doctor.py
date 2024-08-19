from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.admission import admission_doctor_association


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    department_name = Column(String, ForeignKey("departments.name"), index=True)
    admissions = relationship("Admission", secondary=admission_doctor_association, back_populates="doctors")