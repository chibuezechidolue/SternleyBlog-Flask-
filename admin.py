from manage import User,db,app
import datetime
import getpass

# create an admin
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
    admin=User(
        first_name='chief',
        last_name='admin',
        email=email,
        password=password,
        username='admin',
        phone=2345666,
        paid=True,
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now(),
        )
    
    with app.app_context():
        db.session.add(admin)
        db.session.commit()

create_admin()