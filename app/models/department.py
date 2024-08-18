from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.admission import Admission
from app.models.doctor import Doctor
from app.models.patient import Patient


class Department(Base):
    __tablename__ = "departments"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: str = Column(String, unique=True, index=True)
    admission: Mapped[List["Admission"]] = relationship(back_populates="department")
    doctor: Mapped[List["Doctor"]] = relationship(back_populates="department")
    patient: Mapped[List["Patient"]] = relationship(back_populates="department")
