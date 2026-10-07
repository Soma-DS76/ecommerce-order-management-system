from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import get_admin_user
from app.database import get_db
from app.models.user import User
from app.schemas.report import SalesReportResponse
from app.services.report_service import get_sales_report


router = APIRouter()


@router.get('/sales', response_model=SalesReportResponse)
def sales_report( current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return get_sales_report(db)