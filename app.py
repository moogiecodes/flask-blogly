"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'alskdjf094r'

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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
    """Handles 'add user' button."""
    users = User.query.all()

    return render_template('add_user_form.html', users=users)


@app.route('/users/new', methods=['POST'])
def save_new_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url') or None

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    
    return render_template('user_details.html', user=user, posts=user.posts)

    # return (render_template('user_details.html', user=user, posts=user.posts)
    #         if user
    #         else redirect('/users'))
    # if user as precautionary measure disallowing nonexistent user_id

@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit_user_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user_detail(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form.get('first-name')
    user.last_name = request.form.get('last-name')
    user.image_url = request.form.get('image-url') or None

    db.session.commit()
    return redirect('/users')
    
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
        
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('add_post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def save_new_post(user_id):
    title = request.form.get('post-title')
    content = request.form.get('post-content')

    new_post = Post(title=title,
                    content=content,
                    user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def user_post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('post_details.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_user_post(post_id):
    post = Post.query.get_or_404(post_id)
 
    return render_template('edit_post_form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_user_post(post_id):
    post = Post.query.get_or_404(post_id)

    post.title = request.form.get('post-title')
    post.content = request.form.get('post-content')

    db.session.commit()
    return redirect(f'/users/{post.user.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_user_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')

# GET OR 404 ?? FOR USER QUERY 