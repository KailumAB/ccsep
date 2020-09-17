import unittest
from app import app


class FlaskTest(unittest.TestCase):


    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        status_code = response.status_code
        self.assertEquals(200, status_code)

if __name__ == '__main__':
    unittest.main()
