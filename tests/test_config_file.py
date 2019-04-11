import os
import unittest

from config_handler.constants import ConfigKeys
from config_handler.handler import ConfigHandler
from config_handler.config_file import Reader, Writer
from config_handler.exceptions import ConfigHandlerFileReadException


class TestConfigFile(unittest.TestCase):

    def setUp(self):
        self._test_config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ), 'tests', 'test_config.ini'
        )

        self._test_config_ok = ConfigHandler(config_path=self._test_config_path)
        self._test_reader_ok = Reader(self._test_config_ok)
        self._test_writer_ok = Writer(self._test_config_ok)

        self._config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ), 'tests', 'config.ini'
        )

        self._config_ok = ConfigHandler(config_path=self._config_path)
        self._reader_ok = Reader(self._config_ok)
        self._writer_ok = Writer(self._config_ok)

        self._config_bad = ConfigHandler()
        self._reader_bad = Reader(self._config_bad)
        self._writer_bad = Writer(self._config_bad)

    def tearDown(self):
        """Destroy test data"""

    def test_init(self):
        self.assertEqual(self._test_reader_ok._config_handler,
                         self._test_config_ok)
        self.assertEqual(self._test_writer_ok._config_handler,
                         self._test_config_ok)

    def test_check_config_path_exist(self):
        self.assertTrue(self._test_reader_ok._check_config_path_exist())
        self.assertTrue(self._test_writer_ok._check_config_path_exist())

        self.assertFalse(self._reader_bad._check_config_path_exist())
        self.assertFalse(self._writer_bad._check_config_path_exist())

    def test_read_config_file(self):
        config = self._test_reader_ok._read_config_file()

        default_dict = {'send_email': 'true'}
        self.assertEqual(dict(config[ConfigKeys.DEFAULT]), default_dict)

        app1_dict = {'send_email': 'false', 'line_height': '12'}
        self.assertEqual(dict(config['app1']), app1_dict)

        app2_dict = {'send_email': 'true', 'front_page_title': 'Hello World!'}
        self.assertEqual(dict(config['app2']), app2_dict)

        config = self._test_writer_ok._read_config_file()

        default_dict = {'send_email': 'true'}
        self.assertEqual(dict(config[ConfigKeys.DEFAULT]), default_dict)

        app1_dict = {'send_email': 'false', 'line_height': '12'}
        self.assertEqual(dict(config['app1']), app1_dict)

        app2_dict = {'send_email': 'true', 'front_page_title': 'Hello World!'}
        self.assertEqual(dict(config['app2']), app2_dict)

    def test_get_template_path(self):
        template_path = f'{self._test_config_path}.template'
        self.assertEqual(self._test_reader_ok._get_template_path(),
                         template_path)
        self.assertEqual(self._test_writer_ok._get_template_path(),
                         template_path)

    def test_check_config_path(self):
        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._reader_bad.check_config_path()

        self.assertTrue('Config path not set' in str(context.exception))

        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._writer_bad.check_config_path()

        self.assertTrue('Config path not set' in str(context.exception))

        exception_not_raised = True
        try:
            with self.assertRaises(ConfigHandlerFileReadException):
                self._test_reader_ok.check_config_path()
            exception_not_raised = False
        except AssertionError:
            assert exception_not_raised

        exception_not_raised = True
        try:
            with self.assertRaises(ConfigHandlerFileReadException):
                self._test_writer_ok.check_config_path()
            exception_not_raised = False
        except AssertionError:
            assert exception_not_raised

    def test_check_template_path(self):
        msg = f'Template file doesn\'t ' \
            f'exist: {self._reader_bad._config_handler.template_path}'

        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._reader_bad.check_template_path()

        self.assertTrue(msg in str(context.exception))

        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._writer_bad.check_template_path()

        self.assertTrue(msg in str(context.exception))

        exception_not_raised = True
        try:
            with self.assertRaises(ConfigHandlerFileReadException):
                self._test_reader_ok.check_template_path()
            exception_not_raised = False
        except AssertionError:
            assert exception_not_raised

        exception_not_raised = True
        try:
            with self.assertRaises(ConfigHandlerFileReadException):
                self._test_writer_ok.check_template_path()
            exception_not_raised = False
        except AssertionError:
            assert exception_not_raised

    def test_read_template_file(self):
        template_vars = {
            'project_root_path': os.path.join('path', 'to', 'project', 'root')
        }
        config = self._reader_ok.read_template_file(template_vars)

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

    def test_reader_check_config_path(self):
        msg_1 = 'Config path not set'

        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._reader_bad.check_config_path()

        self.assertTrue(msg_1 in str(context.exception))

        exception_not_raised = True
        try:
            with self.assertRaises(ConfigHandlerFileReadException):
                self._test_reader_ok.check_config_path()
            exception_not_raised = False
        except AssertionError:
            assert exception_not_raised

        msg_2 = 'Config file doesn\'t exist: ./config.ini'
        self._reader_bad._config_handler.config_path = './config.ini'

        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._reader_bad.check_config_path()

        self.assertTrue(msg_2 in str(context.exception))

    def test_writer_check_config_path(self):
        msg_1 = 'Config path not set'

        with self.assertRaises(ConfigHandlerFileReadException) as context:
            self._writer_bad.check_config_path()

        self.assertTrue(msg_1 in str(context.exception))

        exception_not_raised = True
        try:
            with self.assertRaises(ConfigHandlerFileReadException):
                self._test_writer_ok.check_config_path()
            exception_not_raised = False
        except AssertionError:
            assert exception_not_raised
