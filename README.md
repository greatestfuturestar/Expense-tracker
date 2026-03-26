# Expense Tracker API

A RESTful API for tracking personal expenses, built as a learning project to practice backend development, PostgreSQL, Docker, and Linux.

## Technologies Used

- Python 3.11 with FastAPI
- PostgreSQL 15
- Docker & Docker Compose
- Raw SQL queries with psycopg2

## Features

- Create and manage multiple users
- Add and delete expenses
- Categorize expenses (food, utilities, transport, etc.)
- Filter expenses by category and date range
- Analytics showing total spending per category

## How to Run

Make sure you have Docker and Docker Compose installed, then:

git clone https://github.com/greatestfuturestar/Expense-tracker.git
cd Expense-tracker
docker-compose up --build

The API will be available at http://localhost:8000

## API Endpoints

- POST /users — create a new user
- POST /expenses — add a new expense
- GET /expenses — get expenses (filter by user_id, category, date_from, date_to)
- DELETE /expenses/{expense_id} — delete an expense
- GET /expenses/analytics — get total spending by category
