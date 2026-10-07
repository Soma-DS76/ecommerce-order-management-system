from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database import base


class Payment(base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    payment_method = Column(String(30), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default='Pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )

    order = relationship('Order', back_populates='payments')