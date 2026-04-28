# ISMS Risk & Vulnerability Management Dashboard

A lightweight web dashboard for tracking information security systems, risks, and vulnerabilities in one place. The project is built with **FastAPI**, **Jinja2 templates**, **SQLAlchemy**, **SQLite**, and **Chart.js**.

It is designed for small security teams, IT departments, students, and companies that want a simple starting point for managing ISMS risk and vulnerability data without needing a large enterprise GRC platform.

## Why This Project Exists

Companies need a clear way to answer practical security questions:

- Which business systems are under security monitoring?
- What risks are linked to each system?
- Which vulnerabilities are still open?
- Which risks are high priority?
- Who owns each system?
- What remediation work is planned?

This dashboard helps turn scattered security notes into a visible workflow. It supports basic ISMS activities such as risk identification, vulnerability tracking, ownership assignment, and remediation planning.

## Features

- Dashboard summary cards for systems, risks, high risks, and open vulnerabilities
- Chart.js visualizations for:
  - exposure by system
  - risk level distribution
  - vulnerability status distribution
- Add and delete systems
- Add and delete risks
- Add and delete vulnerabilities
- Color-coded risk and vulnerability badges
- System dropdowns so risks and vulnerabilities can be linked to real systems
- Clean navigation for overview, records, systems, risks, and vulnerabilities
- SQLite database for local development
- FastAPI routes for both browser forms and API-style list endpoints

## How It Works

The application uses FastAPI as the backend web framework. Data is stored in a local SQLite database through SQLAlchemy models. The dashboard page is rendered with a Jinja2 HTML template, and charts are drawn in the browser using Chart.js.

Basic flow:

1. A user opens `/dashboard`.
2. FastAPI queries systems, risks, and vulnerabilities from SQLite.
3. The backend calculates summary counts and chart data.
4. Jinja2 renders `dashboard.html`.
5. Chart.js uses the rendered JSON data to draw the dashboard charts.
6. Forms submit new records to FastAPI routes.
7. Delete buttons call route handlers that remove records from the database.

## Code Structure

```text
isms-dashboard/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── systems.py
│   │   ├── risks.py
│   │   └── vulnerabilities.py
│   └── templates/
│       └── dashboard.html
├── requirements.txt
├── .gitignore
└── README.md
```

### `app/main.py`

Creates the FastAPI app, initializes the database tables, includes the route files, and renders the dashboard.

Important responsibilities:

- starts the application object
- registers routers
- loads data for the dashboard
- calculates dashboard metrics
- prepares chart data
- redirects `/` to `/dashboard`

### `app/database.py`

Configures the SQLite database connection and SQLAlchemy session.

The project currently uses:

```text
sqlite:///./isms.db
```

That means the database file is created locally as `isms.db` when the app runs.

### `app/models.py`

Defines the database tables:

- `System`
  - `id`
  - `name`
  - `owner`
- `Risk`
  - `id`
  - `description`
  - `likelihood`
  - `impact`
  - `system_id`
- `Vulnerability`
  - `id`
  - `title`
  - `severity`
  - `status`
  - `remediation_plan`
  - `system_id`

Risks and vulnerabilities are linked to systems through `system_id`.

### `app/routes/systems.py`

Handles system records.

Routes include:

- `POST /systems` adds a new system
- `GET /systems` returns all systems
- `POST /systems/{system_id}/delete` deletes a system

When a system is deleted, linked risks and vulnerabilities are also deleted so stale records are not left behind.

### `app/routes/risks.py`

Handles risk records.

Routes include:

- `POST /risks` adds a new risk
- `GET /risks` returns all risks
- `POST /risks/{risk_id}/delete` deletes a risk

Risk score is calculated as:

```text
likelihood * impact
```

Risk levels:

- `Low`: score 1-3
- `Medium`: score 4-6
- `High`: score 7-9

### `app/routes/vulnerabilities.py`

Handles vulnerability records.

Routes include:

- `POST /vulnerabilities` adds a new vulnerability
- `GET /vulnerabilities` returns all vulnerabilities
- `POST /vulnerabilities/{vulnerability_id}/delete` deletes a vulnerability

### `app/templates/dashboard.html`

The main user interface.

It contains:

- page layout
- sidebar navigation
- summary cards
- forms
- tables
- badges
- delete buttons
- Chart.js chart setup
- responsive CSS

## Installation

Clone the repository:

```bash
git clone https://github.com/Sufyann34/isms-dashboard.git
cd isms-dashboard
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard
```

## How To Use It

### 1. Add Company Systems

Start by adding the systems your company wants to monitor, for example:

- Payment Service
- Customer Database
- HR Portal
- Email Gateway
- Cloud Infrastructure
- VPN Service

Each system should have an owner. The owner is usually the person or team responsible for security follow-up.

### 2. Add Risks

For each system, add realistic risk statements.

Example:

```text
Unauthorized access to Payment Service could expose customer transaction data.
```

Choose:

- likelihood from 1 to 3
- impact from 1 to 3
- the affected system

The dashboard automatically calculates the score and level.

### 3. Add Vulnerabilities

Add known vulnerabilities or audit findings.

Example:

```text
Outdated payment API dependency
```

Track:

- severity
- status
- remediation plan
- related system

### 4. Review Dashboard Charts

Use the charts to quickly understand:

- which systems have the most exposure
- whether risk is mostly low, medium, or high
- how many vulnerabilities are open, in progress, or closed

### 5. Clean Up Records

Use the delete buttons when a record is no longer relevant.

Be careful when deleting a system. Deleting a system also deletes the risks and vulnerabilities connected to that system.

## How A Company Can Use This

This dashboard can support common security and compliance workflows:

- Weekly security risk review
- Vulnerability remediation meetings
- ISO 27001 ISMS tracking
- Internal audit preparation
- Ownership mapping for critical systems
- IT risk reporting for management
- Student or training demonstrations of risk management concepts

Suggested company workflow:

1. Security team adds all important business systems.
2. System owners review and confirm their ownership.
3. Risks are added during risk assessment workshops.
4. Vulnerabilities are added from scans, audits, or manual findings.
5. High risks and open vulnerabilities are reviewed weekly.
6. Remediation plans are updated until issues are closed.
7. Dashboard screenshots or exported data can support management reporting.

## Example Use Case: Payment Service

A company running a Payment Service may need to track:

- payment API vulnerabilities
- missing access controls
- weak logging
- delayed patching
- high-impact risks related to customer payment data

This dashboard lets the team connect those risks and vulnerabilities directly to the Payment Service, assign ownership, and keep the remediation plan visible.

## Security Notes

This project is a learning and lightweight internal dashboard. Before using it in production, consider adding:

- authentication and login controls
- role-based access control
- audit logging
- stronger database configuration
- CSRF protection for form actions
- input validation improvements
- backup and restore procedures
- deployment behind HTTPS

Do not expose this app publicly without adding proper security controls.

## Future Improvements

Good next features would include:

- edit buttons for records
- user authentication
- risk owner and due date fields
- vulnerability due dates
- filtering and search
- CSV export
- status history
- database migration support
- PostgreSQL support for production deployment

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- Chart.js
- Uvicorn
