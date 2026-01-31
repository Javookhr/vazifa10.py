from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File
from typing import List, Optional
import uvicorn
from database import Base, engine, get_db
from schemas import *
import crud

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
@app.post("/doctors/", response_model=DoctorResponse)
async def create_doctor_endpoint(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_doctor(doctor, db)

@app.get("/doctors/", response_model=List[DoctorResponse])
async def get_all_doctors_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_doctors(db)

@app.get("/doctors/{doctor_id}", response_model=DoctorResponse)
async def get_doctor_endpoint(doctor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.read_doctor(doctor_id, db)
    except HTTPException:
        raise

@app.put("/doctors/{doctor_id}", response_model=DoctorResponse)
async def update_doctor_endpoint(doctor_id: int, doctor_update: DoctorCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.update_doctor(doctor_id, doctor_update, db)
    except HTTPException:
        raise

@app.delete("/doctors/{doctor_id}")
async def delete_doctor_endpoint(doctor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.delete_doctor(doctor_id, db)
    except HTTPException:
        raise


@app.post("/patients/", response_model=PatientResponse)
async def create_patient_endpoint(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    try:
        await crud.read_doctor(patient.doctor_id, db)
    except HTTPException:
        raise HTTPException(status_code=404, detail="Doktor topilmadi")
    return await crud.patient_create(patient, db)

@app.get("/patients/", response_model=List[PatientResponse])
async def get_all_patients_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_patients(db)

@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient_endpoint(patient_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.read_patient(patient_id, db)
    except HTTPException:
        raise

@app.put("/patients/{patient_id}", response_model=PatientResponse)
async def update_patient_endpoint(patient_id: int, patient_update: PatientCreate, db: AsyncSession = Depends(get_db)):
    if patient_update.doctor_id:
        try:
            await crud.read_doctor(patient_update.doctor_id, db)
        except HTTPException:
            raise HTTPException(status_code=404, detail="Doktor topilmadi")
    try:
        return await crud.update_patient(patient_id, patient_update, db)
    except HTTPException:
        raise

@app.delete("/patients/{patient_id}")
async def delete_patient_endpoint(patient_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.delete_patient(patient_id, db)
    except HTTPException:
        raise


@app.post("/patients/upload/", response_model=PatientResponse)
async def create_patient_with_files_endpoint(
    full_name: str = Form(...),
    birth_date: str = Form(...),
    phone_number: str = Form(...),
    doctor_id: int = Form(...),
 image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        await crud.read_doctor(doctor_id, db)
    except HTTPException:
        raise HTTPException(status_code=404, detail="Doktor topilmadi")

    patient = PatientCreate(
        full_name=full_name,
        birth_date=birth_date,
        phone_number=phone_number,
        doctor_id=doctor_id
    )
    
    return await crud.create_Patient(patient, db, image, video)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)