# 🔐 Secure Task Manager

A security-focused task management web application built with Django 6.0, demonstrating **OWASP Top 10** compliance and **secure coding practices**.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Security Implementation](#-security-implementation)
4. [OWASP Compliance Matrix](#-owasp-compliance-matrix)
5. [Installation & Setup](#-installation--setup)
6. [Usage Guide](#-usage-guide)
7. [Project Structure](#-project-structure)
8. [Security Testing Results](#-security-testing-results)
9. [Screenshots](#-screenshots)
10. [Dependencies](#-dependencies)

---

## 🎯 Project Overview

### Purpose
This application implements a **secure task management system** where users can create, read, update, and delete (CRUD) their personal tasks. The application enforces strict access controls, ensuring users can only manage their own tasks while administrators have oversight capabilities.

### Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Django 6.0 (Python) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Authentication** | Django Auth + django-axes |
| **Password Hashing** | Argon2 (OWASP Recommended) |
| **Frontend** | Bootstrap 5.3 with SRI |

---

## ✨ Features

### User Features
| Feature | Description |
|---------|-------------|
| 📝 **Registration** | Create account with password validation |
| 🔑 **Login/Logout** | Secure authentication with rate limiting |
| ✅ **Task Management** | Create, view, edit, delete personal tasks |
| 👤 **Profile** | View account info and task statistics |

### Admin Features
| Feature | Description |
|---------|-------------|
| 👁️ **View All Tasks** | Oversight of all user tasks |
| 📊 **Audit Log** | Security event monitoring |
| ⚙️ **Admin Panel** | Django admin interface |

### Security Features
- ✅ **Argon2 Password Hashing** (OWASP recommended)
- ✅ **Role-Based Access Control** (RBAC)
- ✅ **Login Rate Limiting** (5 attempts, 2-min lockout)
- ✅ **Session Timeout** (30 minutes)
- ✅ **CSRF Protection** on all forms
- ✅ **SQL Injection Prevention** via Django ORM
- ✅ **XSS Prevention** via template auto-escaping
- ✅ **Custom Error Pages** (no information disclosure)
- ✅ **Comprehensive Audit Logging**
- ✅ **Content Security Policy** (CSP)
- ✅ **Subresource Integrity** (SRI) on CDN resources

---

## 🔒 Security Implementation

### 1. Input Validation (OWASP ASVS V5)
```python
# Server-side validation using Django Forms
class TaskForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 1:
            raise forms.ValidationError("Title cannot be empty.")
        return title
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Date already passed.")
        return due_date
```

### 2. Authentication & Session Management (OWASP ASVS V2)
```python
# settings.py - Security Configuration
PASSWORD_HASHERS = ['django.contrib.auth.hashers.Argon2PasswordHasher', ...]
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Rate Limiting with django-axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 2 / 60  # 2 minutes
```

### 3. Access Control (OWASP ASVS V4)
```python
# RBAC Implementation in Views
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        task = self.get_object()
        # Only owner or admin can update
        return self.request.user == task.owner or self.request.user.is_staff
```

### 4. Error Handling (OWASP ASVS V7)
```python
# Custom error handlers - No stack traces exposed
handler400 = 'securetaskapp.views.custom_400'
handler403 = 'securetaskapp.views.custom_403'
handler404 = 'securetaskapp.views.custom_404'
handler500 = 'securetaskapp.views.custom_500'
```

### 5. Audit Logging (OWASP ASVS V7)
```python
# Automatic logging via Django signals
@receiver(user_logged_in)
def log_successful_login(sender, user, request, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='LOGIN_SUCCESS',
        ip_address=request.META.get('REMOTE_ADDR'),
        details=f"Login via {request.META.get('HTTP_USER_AGENT')}"
    )
```

---

## 📊 OWASP Compliance Matrix

| OWASP Top 10 2021 | Risk | Mitigation | Status |
|-------------------|------|------------|--------|
| **A01** | Broken Access Control | LoginRequiredMixin, UserPassesTestMixin, owner filtering | ✅ |
| **A02** | Cryptographic Failures | Argon2 hashing, HTTPS-ready cookies | ✅ |
| **A03** | Injection | Django ORM, parameterized queries, form validation | ✅ |
| **A04** | Insecure Design | Secure-by-default, input whitelisting | ✅ |
| **A05** | Security Misconfiguration | DEBUG=False, custom error pages, security headers | ✅ |
| **A06** | Vulnerable Components | Snyk scanning, minimal dependencies | ✅ |
| **A07** | Auth Failures | Rate limiting, session timeout, strong hashing | ✅ |
| **A08** | Integrity Failures | CSRF tokens, SRI on CDN resources | ✅ |
| **A09** | Logging Failures | Comprehensive audit logging | ✅ |
| **A10** | SSRF | No external URL fetching | N/A |

---

## 🚀 Installation & Setup

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

# 4. Configure environment (optional)
cp env.example .env
# Edit .env with your settings

# 5. Run database migrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Run development server
DJANGO_DEBUG=True python manage.py runserver
```

### Access the Application
| Page | URL |
|------|-----|
| **Home/Login** | http://127.0.0.1:8000/ |
| **Register** | http://127.0.0.1:8000/register/ |
| **Tasks** | http://127.0.0.1:8000/tasks/ |
| **Admin Panel** | http://127.0.0.1:8000/admin/ |
| **Audit Log** | http://127.0.0.1:8000/tasks/audit-log/ (Admin only) |

---

## 📖 Usage Guide

### For Regular Users
1. **Register** a new account at `/register/`
2. **Login** with your credentials
3. **Create tasks** with title, description, status, and due date
4. **Manage tasks** - edit or delete your own tasks
5. **View profile** to see your task statistics

### For Administrators
1. **Login** with an admin account (is_staff=True)
2. **View all tasks** from all users
3. **Access audit log** to monitor security events
4. **Use admin panel** for user management

### Testing Security Features

| Test | Steps |
|------|-------|
| **Rate Limiting** | Enter wrong password 5 times → See lockout page |
| **Access Control** | Try accessing another user's task → 403 Forbidden |
| **Error Pages** | Visit invalid URL → Custom 404 page (DEBUG=False) |
| **CSRF** | Disable cookies, submit form → CSRF error |

---

## 📁 Project Structure

```
secure-task-manager/
├── securetaskapp/              # Main Django project
│   ├── settings.py             # Security configurations
│   ├── urls.py                 # URL routing + error handlers
│   ├── views.py                # Custom error handlers
│   └── templates/              # Global templates
│       ├── base.html           # Base template with CSP & SRI
│       ├── 400.html            # Bad Request error
│       ├── 403.html            # Forbidden error
│       ├── 404.html            # Not Found error
│       ├── 500.html            # Server Error
│       └── registration/       # Auth templates
│
├── tasks/                      # Task management app
│   ├── models.py               # Task model with owner FK
│   ├── views.py                # CRUD views with RBAC
│   ├── forms.py                # Input validation
│   └── templates/tasks/        # Task templates
│
├── auditlog/                   # Security logging app
│   ├── models.py               # AuditLog model
│   ├── signals.py              # Auth event handlers
│   └── apps.py                 # Signal registration
│
├── requirements.txt            # Python dependencies
├── env.example                 # Environment template
├── manual_code_review_checklist.md  # Security checklist
├── bandit_report.txt           # SAST results
├── snyk_code_report.json       # Code analysis
├── snyk_dependency_report.json # Dependency scan
└── README.md                   # This file
```

---

## 🧪 Security Testing Results

### Static Analysis (Bandit)
```
Run started: 2026-01-18

Test results:
    No issues identified.

Total lines of code: 432
Total issues: 0 (High: 0, Medium: 0, Low: 0)
```

### Dependency Scanning (Snyk)
```
Testing secure-task-manager...

✔ Tested 8 dependencies for known issues
✔ No vulnerable paths found
```

### Dynamic Testing (OWASP ZAP)
| Risk Level | Count |
|------------|-------|
| High | 0 |
| Medium | 0 |
| Low | 2 (Informational) |

---

## 📸 Screenshots

### Login Page
- Clean login form with CSRF protection
- Rate limiting active (django-axes)

### Task List
- User sees only their own tasks
- Admin sees all tasks with owner info

### Audit Log (Admin)
- Login success/failure events
- Task CRUD operations
- IP addresses captured

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | ≥5.0, <7.0 | Web framework |
| django-axes | ≥8.0.0 | Login rate limiting |
| argon2-cffi | ≥23.1.0 | Password hashing |

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Secret key for crypto | dev-only-key |
| `DJANGO_DEBUG` | Debug mode | False |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames | 127.0.0.1,localhost |

### Production Checklist
- [ ] Set `DJANGO_SECRET_KEY` to a unique value
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Enable `CSRF_COOKIE_SECURE=True`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up HTTPS with TLS certificate
- [ ] Configure static file serving (WhiteNoise/nginx)

---

## 👨‍💻 Author

| Field | Value |
|-------|-------|
| **Course** | Secure Software Development |
| **Project** | Secure Microservice-Based Web Application |
| **Framework** | Django 6.0 (Python) |

---

## 📚 References

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP ASVS v4.0](https://owasp.org/www-project-application-security-verification-standard/)
- [Django Security Documentation](https://docs.djangoproject.com/en/5.0/topics/security/)
- [django-axes Documentation](https://django-axes.readthedocs.io/)

---

## 📄 License

This project is for educational purposes as part of the Secure Software Development course.
