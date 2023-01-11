import unittest
import os
from io import BytesIO

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 

if os.environ.get('ROOT_PRJ_DIR') is None:
    print('ROOT_PRJ_DIR must be set before starting\n')
    sys.exit(1)
    

from components.impl.server.app import app

class AppTests(unittest.TestCase):
    def setUp(self):
        print("Running ", self._testMethodName)
        self.ctx = app.app_context()
        self.baseURL = 'http://localhost:5000'
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_report(self):
        response = self.client.get("/report")
        self.assertEqual(response.status_code, 200)

    def test_transactions(self):
        #response = self.client.post("/transactions", data={"data": "data.csv"})
        response = self.client.post('/transactions', data=dict(
                               data=(ROOT_DIR + os.sep + "test_data/data.csv", 'data.csv'),
                           ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists(ROOT_DIR + os.sep + "/../../../../build_output/data.csv"))

if __name__ == "__main__":
    unittest.main()