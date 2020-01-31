from unittest import TestCase
from app import app
from models import User, db

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'


class TestRoutes(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        test_dummy = User(first_name='Test', last_name='Dummy')
        
        db.session.add(test_dummy)

        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_new_user(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_clicked_user(self):
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('alt="User Avatar">', html)
            self.assertIn('<form action="/users/1/edit">', html)

    def test_none_user(self):
        with app.test_client() as client:
            resp = client.get('/users/-1')

            self.assertEqual(resp.status_code, 404)

    def test_add_post_form(self):
        with app.test_client() as client:
            resp = client.get('/users/1/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="post-title">Title</label>', html)

    def test_add_post(self):
        with app.test_client() as client:
            resp = client.post('/users/1/posts/new', data={
                                'post-title': 'Something Long',
                                'post-content': 'Should we do a big block'
                    }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Something Long', html)

            user = User.query.get(1)
            content = user.posts[0].content

            self.assertEqual('Should we do a big block', content)
