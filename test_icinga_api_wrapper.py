import unittest
import icinga_api_wrapper as iaw
from mock import patch

class TestConfig(iaw.Config):
    DEBUG = True
    TESTING = True
    ICINGA_BASE_URL = 'http://my.icinga.host'


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = iaw.create_app(TestConfig)
        self.client = self.app.test_client()


class TestCMD(BaseTest):
    postdata = {
        'cmd_typ': '30',
        'cmd_mod': '2',
        'hostservice': 'host^service',
        'plugin_state': '0',
        'plugin_output': 'output',
        'performance_data': 'perfdata',
    }

    def setUp(self):
        super(TestCMD, self).setUp()

    @patch('icinga_api_wrapper.urllib.urlopen')
    def test_submit_passive_calls_correct_uri(self, urlopen):
        self.client.post('/cmd/submit_passive', data = self.postdata)
        self.assertTrue(urlopen.called)
        called_url = urlopen.call_args[0][0]
        self.assertEqual(TestConfig.ICINGA_BASE_URL + '/cmd.cgi', called_url)


if __name__ == '__main__':
    unittest.main()
