import unittest
from app import app
import datetime

class FlaskTest(unittest.TestCase):

    def make_client(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_ECHO'] = False
        tester = app.test_client(self)
        return tester

    def login(self, client):
        response = client.post('/login', data=dict(
            username='John Smith',
            password='johnpw'
        ), follow_redirects=True)
        status_code = response.status_code
        assert b'Search' in response.data

    def test_admin_get_all_fields(self):
        tester = self.make_client()
        self.login(tester)
        response = tester.get('/admin', data=dict(
            search='*',
            id='2'
        ), follow_redirects=True)
        assert b'username: Ed Williams' in response.data

    def test_admin_cannot_get_password(self):
        tester = self.make_client()
        self.login(tester)

        response = tester.get('/admin', data=dict(
            search='password',
            id='2'
        ), follow_redirects=True)
        assert b'password:' not in response.data

    def test_admin_inject_sleep(self):
        tester = self.make_client()
        self.login(tester)

        now = datetime.datetime.now()
        response = tester.get('/admin', data=dict(
            search='IF(SUBSTRING(password,1,1) = CHAR(101), SLEEP(5), null)', # check if first letter is e
            id='2'
        ), follow_redirects=True)
        later = datetime.datetime.now()
        time_delta = later - now
        assert time_delta.seconds >= 5

        now = datetime.datetime.now()
        response = tester.get('/admin', data=dict(
            search='IF(SUBSTRING(password,1,1) = CHAR(102), SLEEP(5), null)', # check if first letter is not e
            id='2'
        ), follow_redirects=True)
        later = datetime.datetime.now()
        time_delta = later - now
        assert time_delta.seconds <= 1

if __name__ == '__main__':
    unittest.main()
