from app.database import session_local
from app.models.user import User
from app.models.cart import Cart
from app.utils.helpers import hash_password


db = session_local()


def create_admin():
    email = 'admin@gmail.com'

    old_user = db.query(User).filter(User.email == email).first()

    if old_user is not None:
        print('Admin already exists')
        return

    admin = User( full_name='Admin',email=email, password=hash_password('Admin12345'), 
                  role='Admin',is_active=True )

    db.add(admin)
    db.flush()

    cart = Cart( customer_id=admin.id )

    db.add(cart)
    db.commit()

    print('Admin created successfully')


create_admin()
db.close()