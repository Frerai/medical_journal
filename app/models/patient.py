from typing import List


from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.department import Department


class Patient(Base):
    __tablename__ = "patients"


    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    social_security_number = Column(String, unique=True, index=True)
    department: Mapped[List["Department"]] = relationship(back_populates="patient")

