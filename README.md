# Secure Authentication System - DecodeLabs Backend Project 3

## What It Does
A secure authentication system with:
- Password hashing using bcrypt
- JWT token generation on login
- Protected routes with token validation
- User registration

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get JWT token |
| GET | `/profile` | Get user profile (protected) |
| GET | `/protected` | Test protected route |

## How to Run
1. Install: `pip install flask bcrypt pyjwt`
2. Run: `python auth_app.py`
3. Test with Postman

## Author
Aiman Zahoor