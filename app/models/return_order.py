from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database import base


class ReturnOrder(base):
    __tablename__ = 'returns'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True, nullable=False)
    reason = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, default='Requested')
    refund_amount = Column(Numeric(10, 2), nullable=True)
    rejection_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = relationship('Order', back_populates='return_order')