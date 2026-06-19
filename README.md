# Database Integration - DecodeLabs Full Stack Project 3

## What It Does
A REST API with full CRUD operations connected to a SQLite database for student management.

## Schema
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Student name |
| email | String | Unique email |
| age | Integer | Student age |
| course | String | Course name |
| created_at | DateTime | Timestamp |

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API welcome message |
| GET | `/students` | Get all students |
| GET | `/students/<id>` | Get student by ID |
| POST | `/students` | Create a new student |
| PUT | `/students/<id>` | Update a student |
| DELETE | `/students/<id>` | Delete a student |

## How to Run
1. Install: `pip install flask flask-sqlalchemy`
2. Run: `python app.py`
3. Test with Postman or browser

## Author
Aiman Zahoor