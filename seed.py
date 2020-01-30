from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

# add dummy users
megan = User(first_name='Megan', last_name='Choi')
will = User(first_name='Will', last_name='Grover')
deejay = User(first_name='Deejay', last_name='Choi')

db.session.add_all([megan, will, deejay])

db.session.commit()
