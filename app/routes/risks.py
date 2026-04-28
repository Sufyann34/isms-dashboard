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


def calculate_risk(likelihood, impact):
    score = likelihood * impact

    if score <= 3:
        level = "Low"
    elif score <= 6:
        level = "Medium"
    else:
        level = "High"

    return score, level


@router.post("/risks")
def create_risk(
    description: str = Form(...),
    likelihood: int = Form(...),
    impact: int = Form(...),
    system_id: int = Form(...),
    db: Session = Depends(get_db)
):
    risk = models.Risk(
        description=description,
        likelihood=likelihood,
        impact=impact,
        system_id=system_id
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/risks")
def get_risks(db: Session = Depends(get_db)):
    return db.query(models.Risk).all()


@router.post("/risks/{risk_id}/delete")
def delete_risk(risk_id: int, db: Session = Depends(get_db)):
    risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()

    if risk:
        db.delete(risk)
        db.commit()

    return RedirectResponse(url="/dashboard#risks", status_code=303)
