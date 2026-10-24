# Gujarat UCC Digital Public Information Platform

A bilingual (English & Gujarati) digital public information platform and editorial CMS for the Gujarat Uniform Civil Code (UCC) initiative.

## Features

- **Public Information Hub**: Structured legal domain overviews covering Marriage & Divorce, Succession & Inheritance, Maintenance & Alimony, Adoption & Guardianship, and Live-in Relationships.
- **Bilingual Interface**: Seamless language switching between English (`en`) and Gujarati (`gu`).
- **Interactive Explainer System**: Clause-by-clause legal explainers, myths vs. facts breakdown, and before/after legal comparison matrices.
- **Digital Library**: Centralized repository for draft bills, gazette notifications, committee reports, public consultation papers, and judicial precedents.
- **Interactive Legislative Timeline**: Chronological tracking of legislative milestones from committee formulation to implementation.
- **Newsroom & Verification Desk**: Fact-checked updates, press briefings, verified clarifications, and mythbuster briefings.
- **Editorial CMS & Corrections**: Full editorial workflow, review cycles, and public transparency correction register.

## Tech Stack

- **Backend**: Python 3.13, Django 6.0
- **Database**: SQLite (Development) / PostgreSQL compatible
- **Frontend**: Django Templates, Semantic HTML5, Vanilla CSS3 (Custom Responsive Design System)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Zubershekh/ucc.git
cd ucc
```

### 2. Set up a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Seed Initial Platform Data (Optional)
Populate the database with pre-configured legal topics, explainers, timeline events, library documents, news items, and admin credentials:
```bash
python scratch/seed_platform_data.py
```
*Default seeded admin credentials:*
- **Username**: `admin`
- **Password**: `admin1234`

### 6. Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## License

This project is developed for public informational and educational purposes.
