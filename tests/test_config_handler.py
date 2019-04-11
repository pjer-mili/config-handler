import os
import unittest

from config_handler.config_file import Reader
from config_handler.constants import ConfigKeys
from config_handler.handler import ConfigHandler


class TestConfigHandler(unittest.TestCase):

    def setUp(self):
        self._config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ), 'tests', 'config.ini'
        )
        self._config = ConfigHandler(config_path=self._config_path)
        self._reader = Reader(self._config)

    def tearDown(self):
        try:
            os.remove(self._config_path)
        except FileNotFoundError:
            pass

    def test_init(self):
        self.assertEqual(self._config.config_path, self._config_path)

    def test_sync_read(self):
        template_vars = {
            'project_root_path': os.path.join('path', 'to', 'project', 'root')
        }
        config = self._config.sync(template_vars).read()

        self.assertTrue(self._reader._check_config_path_exist())

        default_dict = {'send_email': 'true',
                        'authenticate_user': 'true',
                        'track_user_activity': 'true'}
        self.assertEqual(dict(config[ConfigKeys.DEFAULT]), default_dict)

        app1_dict = {'send_email': 'false',
                     'line_height': '12',
                     'input_path': 'path/to/project/root/input/app1',
                     'track_user_activity': 'false',
                     'authenticate_user': 'true'}
        self.assertEqual(dict(config['app1']), app1_dict)

        app2_dict = {'front_page_title': 'Hello World!',
                     'input_path': 'path/to/project/root/input/app2',
                     'send_email': 'true',
                     'authenticate_user': 'true',
                     'track_user_activity': 'true'}
        self.assertEqual(dict(config['app2']), app2_dict)
