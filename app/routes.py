from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection
from datetime import date

router = APIRouter()

class ExpenseCreate(BaseModel):
    user_id: int
    amount: float
    category: str
    description: str = None
    date: date

class UserCreate(BaseModel):
    username: str


@router.post("/users")
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username) VALUES (%s) RETURNING user_id, username",
            (user.username,)
        )
        new_user = cursor.fetchone()
        conn.commit()
        return {"user_id": new_user[0], "username": new_user[1]}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/expenses")
def add_expense(expense: ExpenseCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO expenses (user_id, amount, category, description, date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING expense_id""",
            (expense.user_id, expense.amount, expense.category, expense.description, expense.date)
        )
        expense_id = cursor.fetchone()[0]
        conn.commit()
        return {"message": "Expense added", "expense_id": expense_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/expenses")
def get_expenses(user_id: int, category: str = None, date_from: date = None, date_to: date = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM expenses WHERE user_id = %s"
        params = [user_id]

        if category:
            query += " AND category = %s"
            params.append(category)

        if date_from:
            query += " AND date >= %s"
            params.append(date_from)

        if date_to:
            query += " AND date <= %s"
            params.append(date_to)

        cursor.execute(query, params)
        expenses = cursor.fetchall()
        return {"expenses": expenses}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_id = %s RETURNING expense_id",
            (expense_id,)
        )
        deleted = cursor.fetchone()
        if not deleted:
            raise HTTPException(status_code=404, detail="Expense not found")
        conn.commit()
        return {"message": "Expense deleted", "expense_id": expense_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/expenses/analytics")
def get_analytics(user_id: int, date_from: date = None, date_to: date = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE user_id = %s
        """
        params = [user_id]

        if date_from:
            query += " AND date >= %s"
            params.append(date_from)

        if date_to:
            query += " AND date <= %s"
            params.append(date_to)

        query += " GROUP BY category ORDER BY total DESC"

        cursor.execute(query, params)
        results = cursor.fetchall()
        return {"analytics": [{"category": row[0], "total": float(row[1])} for row in results]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()