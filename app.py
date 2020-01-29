"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'alskdjf094r'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def base():
    return redirect('/users')


@app.route("/users")
def user_list():
    """Lists all users."""

    users = User.query.all()
    return render_template('index.html', users=users)


@app.route("/users/new")
def add_new_user():
    return render_template('add_user_form.html')


@app.route('/users/new', methods=['POST'])
def save_new_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get(user_id)

    return (render_template('user_details.html', user=user)
            if user
            else redirect('/users'))


@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):
    user = User.query.get(user_id)

    return render_template('edit_user_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user_detail(user_id):
    action = request.form.get('submit')

    if action == 'save':
        user = User.query.get(user_id)

        user.first_name = request.form.get('first-name')
        user.last_name = request.form.get('last-name')
        user.image_url = request.form.get('image-url')

        db.session.commit()

    return redirect(f'/users/{user_id}')
