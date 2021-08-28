import unittest
from source.HTTPResponseSource import HTTPResponseSource

class HTTPResponseSourceTest(unittest.TestCase):
    def test_url_response_success(self):
        url = 'https://istandischeuernochimamt.de/'
        source = HTTPResponseSource(url)

        request_successfull = False

        try:
            source._get_data()
            request_successfull = True
        except:
            request_successfull = False

        self.assertEqual(request_successfull, True)


    def test_url_response_failure(self):
        url = 'not-a-valid-url'
        source = HTTPResponseSource(url)

        request_successfull = False

        with self.assertRaises(ConnectionError):
            source._get_data()
