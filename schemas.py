from pydantic import BaseModel
from typing import Optional
from datetime import date

class DoctorCreate(BaseModel):
    full_name: str
    specialization: str
    phone_number: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    full_name: str
    birth_date: str
    phone_number: str
    doctor_id: int


class PatientResponse(PatientCreate):
    id: int
    image: Optional[str] = None
    video: Optional[str] = None

    class Config:
        from_attributes = True
