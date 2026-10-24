# PostgreSQL Production Architecture & Migration Guide

## 1. Overview
The Gujarat UCC Digital Public Information Platform uses a resilient dual-database configuration:
- **Local / Preview Deployment:** Bundled SQLite (`db.sqlite3` with automatic `/tmp` cold-start copy on Vercel Serverless).
- **Production Architecture:** Managed PostgreSQL (compatible with Neon Serverless Postgres, Supabase, AWS RDS, or Render PostgreSQL).

---

## 2. Dependencies
Ensure `requirements.txt` includes:
```text
Django>=5.0
whitenoise>=6.6.0
dj-database-url>=2.1.0
psycopg2-binary>=2.9.9
```

---

## 3. Environment Configuration
Set the following environment variable in your production hosting environment (e.g., Vercel Project Settings $\rightarrow$ Environment Variables):

```bash
DATABASE_URL="postgresql://username:password@your-db-host.neon.tech/ucc_db?sslmode=require"
DJANGO_SECRET_KEY="your-production-secret-key"
DEBUG="False"
```

When `DATABASE_URL` is detected, `config/settings.py` automatically parses it via `dj_database_url` with persistent connection pooling (`conn_max_age=600`).

---

## 4. Production Migration Steps

### Step 1: Run Migrations on PostgreSQL
Connect your shell to the production database environment and execute:
```bash
python manage.py migrate
```
This applies all 12 app migrations:
1. `core` (SiteSettings, UserProfile, UserRole, AuditLog)
2. `topics` (Legal Topic Taxonomy)
3. `explainers` (Plain-Language Guides, Statutory Citations, Advocate Attributions)
4. `library` (Acts, Gazettes, Rules, Court Judgments)
5. `timeline` (Legislative Milestones)
6. `news` (Verified Updates, Fact Checks)
7. `glossary_faq` (Statutory Terms & Citizen Questions)
8. `corrections` (Public Correction Intake Queue)
9. Standard Django apps (`auth`, `admin`, `sessions`, `contenttypes`)

---

### Step 2: Seed Official Legal Data & Admin Users
To populate the production PostgreSQL database with the complete statutory content and default admin accounts:
```bash
python scratch/seed_platform_data.py
```
This creates:
- Superuser: `admin` (Password: `admin1234` - *change immediately upon first login*)
- Site Settings with verified status: **Published in Gazette (૧૭ સપ્ટેમ્બર ૨૦૨૬ રાષ્ટ્રપતિ મંજૂરી / ૧ ઓક્ટોબર ૨૦૨૬ અસાધારણ ગેઝેટ)**
- 6 Core Subject Topics
- Plain-Language Explainers with Section Citations & Advocate QA Notes
- Official Gazette Documents (Gujarat Act 17 of 2026, Assembly Bill 17/2026)
- 15+ Legislative Timeline milestones
- Fact-Checked News articles & Mythbusters

---

### Step 3: (Alternative) Direct SQLite to PostgreSQL Dump
If migrating existing local database state directly:
```bash
# 1. Dump current SQLite data to JSON
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > datadump.json

# 2. Switch DATABASE_URL to PostgreSQL, run migrations
python manage.py migrate

# 3. Load data into PostgreSQL
python manage.py loaddata datadump.json
```

---

## 5. Security & Verification Guardrails
- **Legal Claim Integrity:** Never mark the Act status as `IN_FORCE` until the State Government officially publishes the Section 1(2) commencement notification in the Gujarat Government Gazette.
- **Role Permissions:** Ensure all legal advocate reviewers have their Bar Council Enrollment Number recorded in `/portal-admin/roles/`.
