import unittest
import icinga_api_wrapper as iaw
from mock import patch
import urlparse

class TestConfig(iaw.Config):
    DEBUG = True
    TESTING = True
    ICINGA_BASE_URL = 'http://my.icinga.host/icinga/'


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = iaw.create_app(TestConfig)
        self.client = self.app.test_client()


class TestCMD(BaseTest):
    postdata = {
        'host': 'myhost',
        'service': 'myservice',
        'result': 'ok',
        'output': 'output',
        'perfdata': 'perfdata',
    }

    def setUp(self):
        super(TestCMD, self).setUp()

    @patch('icinga_api_wrapper.urllib.urlopen')
    def test_submit_passive_calls_correct_uri(self, urlopen):
        self.client.post('/cmd/submit_passive', data = self.postdata)
        self.assertTrue(urlopen.called)
        called_url = urlopen.call_args[0][0]
        self.assertEqual(TestConfig.ICINGA_BASE_URL + 'cmd.cgi', called_url)

    @patch('icinga_api_wrapper.urllib.urlopen')
    def test_submit_passive_sends_correct_data(self, urlopen):
        self.client.post('/cmd/submit_passive', data = self.postdata)
        self.assertTrue(urlopen.called)
        data = urlparse.parse_qsl(urlopen.call_args[0][1])
        data = dict(data)
        self.assertEqual(
            {
                'cmd_typ': '30',
                'cmd_mod': '2',
                'hostservice': self.postdata['host'] + '^' + self.postdata['service'],
                'plugin_state': '0',
                'plugin_output': self.postdata['output'],
                'performance_data': self.postdata['perfdata'],
            },
            data,
        )


if __name__ == '__main__':
    unittest.main()
