from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/systems")
def create_system(
    name: str = Form(...),
    owner: str = Form(...),
    db: Session = Depends(get_db)
):
    system = models.System(name=name, owner=owner)

    db.add(system)
    db.commit()
    db.refresh(system)

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/systems")
def get_systems(db: Session = Depends(get_db)):
    return db.query(models.System).all()


@router.post("/systems/{system_id}/delete")
def delete_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()

    if system:
        db.query(models.Risk).filter(models.Risk.system_id == system_id).delete()
        db.query(models.Vulnerability).filter(
            models.Vulnerability.system_id == system_id
        ).delete()
        db.delete(system)
        db.commit()

    return RedirectResponse(url="/dashboard#systems", status_code=303)
