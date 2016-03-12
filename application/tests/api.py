import json
import re
import sys
import unittest

from app.settings import create_app
from flask import request

sys.path.append('..')


class APITest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config/test.cfg', False)
        self.app.config['TESTING'] = True

    def tearDown(self):
        # mongo.db.drop_database('test')
        request.environ.get('werkzeug.server.shutdown')

    def testnoroot(self):
        response = self.app.test_client().get("/")
        self.assertTrue(response.status_code == 404)

    def testgoodjson(self):
        f = open("tests/test.json", "r")
        payload = json.load(f)
        response = self.app.test_client().post("/store", data=payload)
        self.assertTrue(response.status_code == 200)

    def testbadchecksum(self):
        f = open("tests/test_wrongcksum.json", "r")
        payload = json.load(f)
        response = self.app.test_client().post("/store", json=payload)
        self.assertTrue(response.status_code == 400)
        r = re.compile("md5", re.IGNORECASE)
        self.assertTrue(r.search(response.content) is not None)

if __name__ == '__main__':
    unittest.main()
