#!/usr/bin/python
# -*- coding: utf-8 -*-
""" unittests for openssl_ca_handler """
import unittest
import sys
import os
import unittest
import requests
from requests.exceptions import HTTPError

try:
    from mock import patch, MagicMock, Mock
except ImportError:
    from unittest.mock import patch, MagicMock, Mock
sys.path.insert(0, '..')


class TestACMEHandler(unittest.TestCase):
    """ test class for cgi_handler """

    def setUp(self):
        """ setup unittest """
        import logging
        from examples.ca_handler.openssl_ca_handler import CAhandler
        logging.basicConfig(
            # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            format='%(asctime)s - acme2certifier - %(levelname)s - %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO)
        self.logger = logging.getLogger('test_acme2certifier')
        self.cahandler = CAhandler(False, self.logger)

    def test_001_default(self):
        """ default test which always passes """
        self.assertEqual('foo', 'foo')

    def test_002_check_config(self):
        """ CAhandler.check_config with an empty config_dict """
        self.cahandler.issuer_dict = {}
        self.assertEqual('key "key" does not exist in config_hash', self.cahandler.check_config())

    def test_003_check_config(self):
        """ CAhandler.check_config with key in config_dict but not existing """
        self.cahandler.issuer_dict = {'key': 'foo.pem'}
        self.assertEqual('signing key foo.pem does not exist', self.cahandler.check_config())

    @patch('os.path.exists')
    def test_004_check_config(self, mock_exists):
        """ CAhandler.check_config with key in config_dict key is existing """
        self.cahandler.issuer_dict = {'key': 'foo'}
        mock_exists.return_value = True
        self.assertEqual('key "cert" does not exist in config_hash', self.cahandler.check_config())

    @patch('os.path.exists')
    def test_005_check_config(self, mock_exists):
        """ CAhandler.check_config with key and cert in config_dict """
        self.cahandler.issuer_dict = {'key': 'foo', 'cert': 'bar'}
        mock_exists.return_value = True
        self.assertFalse(self.cahandler.check_config())

if __name__ == '__main__':

    if os.path.exists('acme_test.db'):
        os.remove('acme_test.db')
    unittest.main()