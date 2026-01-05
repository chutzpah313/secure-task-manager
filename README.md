# Secure Task Manager

A secure task management application built with Django, following OWASP security guidelines.

## Features

- ✅ User authentication (login, logout, register)
- ✅ Role-based access control (Admin/Staff vs Regular users)
- ✅ Full CRUD for tasks (Create, Read, Update, Delete)
- ✅ Audit logging for all actions
- ✅ OWASP-compliant security settings
- ✅ Bootstrap 5 responsive UI

## Security Features

- Argon2 password hashing
- CSRF protection
- Session security (HttpOnly cookies)
- X-Frame-Options: DENY
- User ownership validation for tasks
- Admin-only audit log access

## Requirements

- Python 3.10+
- Django 5.0+

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/chutzpah313/secure-task-manager.git
cd secure-task-manager
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Access the app
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
secure-task-manager/
├── manage.py
├── requirements.txt
├── securetaskapp/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── templates/
│       ├── base.html
│       ├── registration/
│       │   ├── login.html
│       │   └── register.html
│       ├── tasks/
│       │   ├── task_list.html
│       │   ├── task_form.html
│       │   └── task_confirm_delete.html
│       └── auditlog/
│           └── audit_log.html
├── tasks/                  # Tasks app
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── auditlog/              # Audit logging app
    ├── models.py
    ├── signals.py
    └── admin.py
```

## Usage

### Regular Users
- Register/Login to access your tasks
- Create, edit, and delete your own tasks
- View only your tasks

### Admin Users
- View all users' tasks
- Edit/delete any task
- Access audit log at `/tasks/audit-log/`
- Access Django admin at `/admin/`

## License

MIT License
