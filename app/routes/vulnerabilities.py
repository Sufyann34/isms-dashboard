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


@router.post("/vulnerabilities")
def create_vulnerability(
    title: str = Form(...),
    severity: str = Form(...),
    status: str = Form(...),
    remediation_plan: str = Form(...),
    system_id: int = Form(...),
    db: Session = Depends(get_db)
):
    vulnerability = models.Vulnerability(
        title=title,
        severity=severity,
        status=status,
        remediation_plan=remediation_plan,
        system_id=system_id
    )

    db.add(vulnerability)
    db.commit()
    db.refresh(vulnerability)

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/vulnerabilities")
def get_vulnerabilities(db: Session = Depends(get_db)):
    return db.query(models.Vulnerability).all()


@router.post("/vulnerabilities/{vulnerability_id}/delete")
def delete_vulnerability(vulnerability_id: int, db: Session = Depends(get_db)):
    vulnerability = db.query(models.Vulnerability).filter(
        models.Vulnerability.id == vulnerability_id
    ).first()

    if vulnerability:
        db.delete(vulnerability)
        db.commit()

    return RedirectResponse(url="/dashboard#vulnerabilities", status_code=303)
