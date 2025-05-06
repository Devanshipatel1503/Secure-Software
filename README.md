# Secure-Software
# 💳 Secure Flask Banking App

A simple Flask-based web application simulating a secure online banking system. It demonstrates login authentication, account balance viewing, and money transfer functionality with built-in protections against common web vulnerabilities like CSRF and XSS.

---

## 🔧 Features

- User login with hashed passwords (using `passlib`)
- JWT-based authentication stored in secure cookies
- CSRF protection on all forms (via `Flask-WTF`)
- Account balance view and money transfer form
- SQLite-backed database storage
- Clean separation of business logic and views

---

## 🔐 Security Features

- ✅ CSRF Protection (`Flask-WTF`)
- ✅ Password hashing using PBKDF2 (`passlib`)
- ✅ JWT Auth Tokens (stored in HTTP-only cookies)
- ✅ Secure cookie flags (`Secure`, `HttpOnly`, `SameSite`)
- ❌ XSS avoided by using template auto-escaping (Jinja2)

---

## 📂 Project Structure

├── app.py # Main Flask app with route definitions
├── user_service.py # Auth handling: login, JWT creation, session check
├── bin/
│ └── account_service.py # Functions for balance check and fund transfers
├── genericforms.py # Flask-WTF forms (LoginForm, TransferForm)
├── templates/ # HTML templates (login, dashboard, etc.)
│ ├── login.html
│ ├── dashboard.html
│ ├── transfer.html
│ └── details.html
├── static/ # Static files (if needed)
├── bank.db # SQLite database file
└── README.md # This documentation file
