from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .routes import systems, risks, vulnerabilities
from . import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(systems.router)
app.include_router(risks.router)
app.include_router(vulnerabilities.router)

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    systems_data = db.query(models.System).all()
    risks_data = db.query(models.Risk).all()
    vulnerabilities_data = db.query(models.Vulnerability).all()
    system_names = {system.id: system.name for system in systems_data}

    risk_levels = {"Low": 0, "Medium": 0, "High": 0}
    for risk in risks_data:
        score = risk.likelihood * risk.impact
        if score <= 3:
            risk_levels["Low"] += 1
        elif score <= 6:
            risk_levels["Medium"] += 1
        else:
            risk_levels["High"] += 1

    vulnerability_statuses = {}
    vulnerability_severities = {}
    for vuln in vulnerabilities_data:
        status = (vuln.status or "Unknown").strip().title()
        severity = (vuln.severity or "Unknown").strip().title()
        vulnerability_statuses[status] = vulnerability_statuses.get(status, 0) + 1
        vulnerability_severities[severity] = vulnerability_severities.get(severity, 0) + 1

    systems_chart = []
    for system in systems_data:
        risk_count = len([risk for risk in risks_data if risk.system_id == system.id])
        vulnerability_count = len([
            vuln for vuln in vulnerabilities_data if vuln.system_id == system.id
        ])
        systems_chart.append({
            "name": system.name,
            "risks": risk_count,
            "vulnerabilities": vulnerability_count,
        })

    context = {
        "request": request,
        "systems": systems_data,
        "risks": risks_data,
        "vulnerabilities": vulnerabilities_data,
        "system_names": system_names,
        "total_systems": len(systems_data),
        "total_risks": len(risks_data),
        "high_risks": risk_levels["High"],
        "open_vulnerabilities": vulnerability_statuses.get("Open", 0),
        "risk_levels": risk_levels,
        "vulnerability_statuses": vulnerability_statuses,
        "vulnerability_severities": vulnerability_severities,
        "systems_chart": systems_chart,
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=context
    )
