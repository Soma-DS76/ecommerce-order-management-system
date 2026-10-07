from fastapi import FastAPI
from sqlalchemy import text

from app.database import session_local
from app.routers.auth import router as auth_router
from app.routers.categories import router as category_router
from app.routers.products import router as product_router
from app.routers.cart import router as cart_router
from app.routers.address import router as address_router
from app.routers.orders import router as order_router
from app.routers.admin_orders import router as admin_order_router
from app.routers.payments import router as payment_router
from app.routers.returns import router as return_router
from app.routers.admin_returns import router as admin_return_router
from app.routers.reviews import router as review_router
from app.routers.reports import router as report_router


app = FastAPI( title='E-Commerce Order Management System', version='1.0.0' )


app.include_router( auth_router, prefix='/auth', tags=['Authentication'] )
app.include_router( category_router,prefix='/categories',tags=['Categories'])
app.include_router( product_router,prefix='/products',tags=['Products'])
app.include_router( cart_router, prefix='/cart', tags=['Cart'] )
app.include_router( address_router, prefix='/addresses', tags=['Addresses'] )
app.include_router( order_router, prefix='/orders', tags=['Orders'] )
app.include_router( admin_order_router, prefix='/admin/orders',tags=['Admin Orders'] )
app.include_router(payment_router, prefix='/payments',tags=['Payments'])
app.include_router(return_router, prefix='/returns', tags=['Returns'])
app.include_router(admin_return_router, prefix='/admin/returns', tags=['Admin Returns'])
app.include_router(review_router, prefix='/reviews', tags=['Reviews'])
app.include_router(report_router, prefix='/reports', tags=['Reports'])


@app.get('/')
def home():
    return { 'message': 'E-Commerce Order Management API is running' }


@app.get('/database-test')
def database_test():
    db = session_local()

    try:
        db.execute(text('SELECT 1'))

        return { 'message': 'Database connection successful' }

    finally:
        db.close()