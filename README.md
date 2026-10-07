# E-Commerce Order Management System

A backend API for managing users, products, categories, carts, orders, payments, returns, reviews, and sales reports.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- MySQL
- Alembic
- JWT Authentication
- Passlib
- bcrypt
- SMTP
- BackgroundTasks
- Uvicorn

## Project Structure

```text
E-Commerce Order Management System/
│
├── app/
│   ├── auth/
│   │   ├── dependencies.py
│   │   └── jwt.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── address.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── return_order.py
│   │   └── review.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── addresses.py
│   │   ├── orders.py
│   │   ├── admin_orders.py
│   │   ├── payments.py
│   │   ├── returns.py
│   │   ├── admin_returns.py
│   │   ├── reviews.py
│   │   └── reports.py
│   │
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── screenshots/
│
├── create_admin.py
├── alembic.ini
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt