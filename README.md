# Secure Task Manager

A security-focused task management web application built with Django, demonstrating OWASP Top 10 compliance and secure coding practices.

## Student Information

| Field | Value |
|-------|-------|
| **Course** | Secure Software Development |
| **Project** | Web Application Security Implementation |
| **Framework** | Django 6.0 (Python) |

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Security Architecture](#security-architecture)
3. [OWASP Compliance Matrix](#owasp-compliance-matrix)
4. [Installation & Setup](#installation--setup)
5. [Application Features](#application-features)
6. [Security Testing Results](#security-testing-results)
7. [File Structure](#file-structure)

---

## Project Overview

### Purpose
This application implements a secure task management system where users can create, read, update, and delete (CRUD) their personal tasks. The application enforces strict access controls, ensuring users can only manage their own tasks while administrators have broader oversight capabilities.

### Key Security Features
- ✅ Secure Authentication with Argon2 password hashing
- ✅ Role-Based Access Control (RBAC) - Admin and User roles
- ✅ Session Management with 30-minute timeout
- ✅ Login Rate Limiting (5 attempts, 2-minute lockout)
- ✅ Comprehensive Audit Logging
- ✅ Custom Error Pages (no information disclosure)
- ✅ CSRF Protection on all forms
- ✅ SQL Injection Prevention via Django ORM
- ✅ XSS Prevention via template auto-escaping

---

## Security Architecture

### Authentication & Session Management

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                       │
├─────────────────────────────────────────────────────────────┤
│  User → Login Form → django-axes (rate limit check)         │
│           ↓                                                  │
│  Password → Argon2 Hash Verification                        │
│           ↓                                                  │
│  Success → Session Created (30-min timeout)                  │
│           ↓                                                  │
│  Audit Log Entry Created                                     │
└─────────────────────────────────────────────────────────────┘
```

| Setting | Value | Purpose |
|---------|-------|---------|
| Password Hasher | Argon2 | OWASP recommended, memory-hard |
| Session Timeout | 30 minutes | Reduces session hijacking window |
| Rate Limiting | 5 attempts / 2 min | Brute force protection |
| CSRF Protection | Enabled | Prevents cross-site request forgery |

### Access Control Model

```
┌─────────────────────────────────────────────────────────────┐
│                    RBAC IMPLEMENTATION                       │
├─────────────────────────────────────────────────────────────┤
│  ADMIN (is_staff=True):                                      │
│    - View all tasks (read-only)                              │
│    - Access audit logs                                       │
│    - Cannot modify other users' tasks                        │
│                                                              │
│  USER (is_staff=False):                                      │
│    - Create own tasks                                        │
│    - Read own tasks only                                     │
│    - Update own tasks only                                   │
│    - Delete own tasks only                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## OWASP Compliance Matrix

| OWASP Top 10 2021 | Vulnerability | Implementation | Status |
|-------------------|---------------|----------------|--------|
| A01:2021 | Broken Access Control | LoginRequiredMixin, UserPassesTestMixin, owner-based filtering | ✅ |
| A02:2021 | Cryptographic Failures | Argon2 password hashing, HTTPS headers configured | ✅ |
| A03:2021 | Injection | Django ORM (parameterized queries), form validation | ✅ |
| A04:2021 | Insecure Design | Secure-by-default architecture, input whitelisting | ✅ |
| A05:2021 | Security Misconfiguration | DEBUG=False, custom error pages, security headers | ✅ |
| A06:2021 | Vulnerable Components | Snyk dependency scanning, minimal dependencies | ✅ |
| A07:2021 | Auth Failures | Rate limiting, session timeout, Argon2 hashing | ✅ |
| A08:2021 | Integrity Failures | CSRF tokens, form validation | ✅ |
| A09:2021 | Logging Failures | Comprehensive audit logging with IP capture | ✅ |
| A10:2021 | SSRF | No external URL fetching implemented | N/A |

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment support

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd secure-task-manager

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

### Access the Application
- **Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Application Features

### User Features
| Feature | Description | Security Control |
|---------|-------------|------------------|
| Registration | Create new account | Password validation, unique email |
| Login | Authenticate to system | Rate limiting, audit logging |
| Task List | View personal tasks | Owner-based filtering |
| Create Task | Add new task | CSRF protection, input validation |
| Edit Task | Modify own task | Ownership verification |
| Delete Task | Remove own task | Ownership verification, confirmation |
| Profile | View account info | Authentication required |

### Admin Features
| Feature | Description | Security Control |
|---------|-------------|------------------|
| View All Tasks | See all users' tasks | is_staff check |
| Audit Log | View security events | is_staff check |
| Admin Panel | Django admin access | is_superuser check |

---

## Security Testing Results

### Static Analysis (Bandit)

```
Run started: 2025-01-XX

Test results:
    No issues identified.

Code scanned:
    Total lines of code: 432
    Total lines skipped: 0

Run metrics:
    Total issues (by severity):
        Undefined: 0
        Low: 0
        Medium: 0
        High: 0
```

### Dependency Scanning (Snyk)

```
Testing /home/aleen/secure-task-manager...

Organization: [username]
Package manager: pip
Target file: requirements.txt

✔ Tested 8 dependencies for known issues
✔ No vulnerable paths found
```

### Security Headers Configured

| Header | Value | Purpose |
|--------|-------|---------|
| X-Frame-Options | DENY | Clickjacking prevention |
| X-Content-Type-Options | nosniff | MIME sniffing prevention |
| Content-Security-Policy | default-src 'self' | XSS prevention |
| Referrer-Policy | same-origin | Information leakage prevention |

---

## File Structure

```
secure-task-manager/
├── securetaskapp/              # Main Django project
│   ├── settings.py             # Security configurations
│   ├── urls.py                 # URL routing
│   └── templates/              # Global templates
│       ├── base.html           # Base template
│       ├── 400.html            # Bad Request error
│       ├── 403.html            # Forbidden error
│       ├── 404.html            # Not Found error
│       └── 500.html            # Server Error
│
├── tasks/                      # Task management app
│   ├── models.py               # Task model (with owner FK)
│   ├── views.py                # CRUD views with RBAC
│   ├── forms.py                # Input validation
│   ├── urls.py                 # App routes
│   └── templates/tasks/        # Task templates
│
├── auditlog/                   # Security logging app
│   ├── models.py               # AuditLog model
│   ├── signals.py              # Auth event handlers
│   └── apps.py                 # Signal registration
│
├── requirements.txt            # Python dependencies
├── bandit_report.txt           # SAST results
└── README.md                   # This file
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 6.0 | Web framework |
| django-axes | 8.1.0 | Login rate limiting |
| argon2-cffi | latest | Password hashing |
| whitenoise | latest | Static file serving |

---

## Security Configuration Summary

### settings.py Security Settings

```python
# Password Hashing - OWASP recommended
PASSWORD_HASHERS = ['django.contrib.auth.hashers.Argon2PasswordHasher', ...]

# Session Security
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True  # HTTPS only in production

# Rate Limiting (django-axes)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=2)
AXES_LOCKOUT_TEMPLATE = 'registration/lockout.html'

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

## Testing the Application

### Test Rate Limiting
1. Navigate to login page
2. Enter incorrect password 5 times
3. Observe lockout page displayed
4. Wait 2 minutes, retry

### Test Access Control
1. Login as regular user
2. Try to access `/audit-log/` - should be denied (403)
3. Login as admin (is_staff=True)
4. Access `/audit-log/` - should succeed

### Test Error Pages
- `/test-400/` - Custom 400 error
- `/test-403/` - Custom 403 error
- `/test-500/` - Custom 500 error
- Any invalid URL - Custom 404 error

---

## Acknowledgments

- OWASP Top 10 2021 Guidelines
- Django Security Documentation
- OWASP ASVS v4.0 (Application Security Verification Standard)
