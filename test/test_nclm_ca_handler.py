#!/usr/bin/python
# -*- coding: utf-8 -*-
""" unittests for acme2certifier """
# pylint: disable= C0415, W0212
import unittest
import sys
import os
from unittest.mock import patch, Mock
import requests

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class TestACMEHandler(unittest.TestCase):
    """ test class for cgi_handler """

    def setUp(self):
        """ setup unittest """
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_a2c')
        from examples.ca_handler.nclm_ca_handler import CAhandler
        self.cahandler = CAhandler(False, self.logger)
        # self.cahandler.api_host = 'api_host'
        # self.cahandler.auth = 'auth'

    def test_001_default(self):
        """ default test which always passes """
        self.assertEqual('foo', 'foo')

    @patch.object(requests, 'post')
    def test_002__api_post(self, mock_req):
        """ test _api_post successful run """
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'foo': 'bar'}
        self.assertEqual({'foo': 'bar'}, self.cahandler._api_post('url', 'data'))

    @patch('requests.post')
    def test_003__api_post(self, mock_post):
        """ CAhandler.get_ca() returns an http error """
        self.cahandler.api_host = 'api_host'
        self.cahandler.auth = 'auth'
        mock_post.side_effect = Exception('exc_api_post')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual('exc_api_post', self.cahandler._api_post('url', 'data'))
        self.assertIn('ERROR:test_a2c:CAhandler._api_post() returned error: exc_api_post', lcm.output)

    @patch('requests.get')
    def test_004_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns nothing """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:ca_id.lookup() no CAs found in response ...', lcm.output)

    @patch('requests.get')
    def test_005_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns wrong data """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'foo': 'bar'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:ca_id.lookup() no CAs found in response ...', lcm.output)

    @patch('requests.get')
    def test_006_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns wrong data """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'foo': 'bar'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:ca_id.lookup() no CAs found in response ...', lcm.output)

    @patch('requests.get')
    def test_007_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns empty ca-list """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': []}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:_ca_id_lookup(): no ca id found for ca_name', lcm.output)

    @patch('requests.get')
    def test_008_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns wrong ca-list """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'foo': 'foo'}]}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:_ca_id_lookup(): no ca id found for ca_name', lcm.output)

    @patch('requests.get')
    def test_009_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns ca-list with name not matching """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'name': 'foo'}]}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:_ca_id_lookup(): no ca id found for ca_name', lcm.output)

    @patch('requests.get')
    def test_010_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns ca-list with name matching  but no id """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'name': 'ca_name'}]}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:_ca_id_lookup(): no ca id found for ca_name', lcm.output)

    @patch('requests.get')
    def test_011_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns ca-list with name matching  and id """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'name': 'ca_name', 'id': 'id'}]}
        self.assertEqual('id', self.cahandler._ca_id_lookup())

    @patch('requests.get')
    def test_012_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns ca-list with desc not matching """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'desc': 'foo'}]}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:_ca_id_lookup(): no ca id found for ca_name', lcm.output)

    @patch('requests.get')
    def test_013_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns ca-list with desc matching  but no id """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'desc': 'ca_name'}]}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._ca_id_lookup())
        self.assertIn('ERROR:test_a2c:_ca_id_lookup(): no ca id found for ca_name', lcm.output)

    @patch('requests.get')
    def test_014_ca_id_lookup(self, mock_req):
        """ CAhandler._ca_id_lookup() returns ca-list with desc matching  and id """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.headers = 'headers'
        mockresponse = Mock()
        mock_req.return_value = mockresponse
        mockresponse.json = lambda: {'CAs': [{'desc': 'ca_name', 'id': 'id'}]}
        self.assertEqual('id', self.cahandler._ca_id_lookup())

    @patch('requests.get')
    def test_015_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns everything with one ca cert """
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'certificate': {'der': 'der', 'pem': 'pem', 'issuerInfo': {'id': 'id'}}}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'certificate': {'pem': 'pemca'}}
        mock_get.side_effect = [mockresponse1, mockresponse2]
        self.assertEqual((None, 'pempemca', 'der'), self.cahandler._cert_bundle_build('foo'))

    @patch('requests.get')
    def test_016_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns everything with two ca cert """
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'certificate': {'der': 'der', 'pem': 'pem', 'issuerInfo': {'id': 'id1'}}}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'certificate': {'pem': 'pemca1', 'issuerInfo': {'id': 'id'}}}
        mockresponse3 = Mock()
        mockresponse3.json = lambda: {'certificate': {'pem': 'pemca2', 'issuerInfo': {'id': 'id'}}}
        mock_get.side_effect = [mockresponse1, mockresponse2, mockresponse3]
        self.assertEqual((None, 'pempemca1pemca2', 'der'), self.cahandler._cert_bundle_build('foo'))

    @patch('requests.get')
    def test_017_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns everything without der in cert_dic """
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'certificate': {'pem': 'pem', 'issuerInfo': {'id': 'id'}}}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'certificate': {'pem': 'pemca'}}
        mock_get.side_effect = [mockresponse1, mockresponse2]
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('no der certificate returned for id foo', 'pempemca', None), self.cahandler._cert_bundle_build('foo'))
        self.assertIn('ERROR:test_a2c:CAhandler._cert_bundle_build(): no der certificate returned for id: foo', lcm.output)

    @patch('requests.get')
    def test_018_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns everything without pem in cert_dic """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_id_list = [1]
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'certificate': {'der': 'der', 'issuerInfo': {'id': 'id'}}}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'certificate': {'pem': 'pemca'}}
        mock_get.side_effect = [mockresponse1, mockresponse2]
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('no pem certificate returned for id foo', 'pemca', 'der'), self.cahandler._cert_bundle_build('foo'))
        self.assertIn('ERROR:test_a2c:CAhandler._cert_bundle_build(): no pem certificate returned for id: foo', lcm.output)

    @patch('requests.get')
    def test_019_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns everything without pem in ca_dic """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_id_list = [1]
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'certificate': {'der': 'der', 'pem': 'pem', 'issuerInfo': {'id': 'id'}}}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'certificate': {'foo': 'bar'}}
        mock_get.side_effect = [mockresponse1, mockresponse2]
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('no pem certificate returned for id id', 'pem', 'der'), self.cahandler._cert_bundle_build('foo'))
        self.assertIn('ERROR:test_a2c:CAhandler._cert_bundle_build(): no pem certificate returned for id: id', lcm.output)

    @patch('requests.get')
    def test_020_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns wrong ca_dic """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_id_list = [1]
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'certificate': {'der': 'der', 'pem': 'pem', 'issuerInfo': {'id': 'id'}}}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'foo': 'bar'}
        mock_get.side_effect = [mockresponse1, mockresponse2]
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('invalid reponse returned for id: id', 'pem', 'der'), self.cahandler._cert_bundle_build('foo'))
        self.assertIn('ERROR:test_a2c:CAhandler._cert_bundle_build(): invalid reponse returned for id: id', lcm.output)

    @patch('requests.get')
    def test_021_ca_id_lookup(self, mock_get):
        """ CAhandler._cert_bundle_build() returns wrong cert_dic """
        self.cahandler.api_host = 'api_host'
        self.cahandler.ca_id_list = [1]
        mockresponse1 = Mock()
        mockresponse1.json = lambda: {'foo': 'bar'}
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'foo': 'bar'}
        mock_get.side_effect = [mockresponse1, mockresponse2]
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('invalid reponse returned for id: foo', None, None), self.cahandler._cert_bundle_build('foo'))
        self.assertIn('ERROR:test_a2c:CAhandler._cert_bundle_build(): invalid reponse returned for id: foo', lcm.output)

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_022_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - one cert - ok """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'subjectAltName': 'subjectAltName', 'certificateId': 'certificateId'}]}
        mock_req.return_value = mockresponse
        mock_comp.return_value = True
        self.assertEqual('certificateId', self.cahandler._cert_id_lookup('csr_cn', 'san_list'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_023_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - two certs - 1st match """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'subjectAltName': 'subjectAltName1', 'certificateId': 'certificateId1'}, {'subjectAltName': 'subjectAltName2', 'certificateId': 'certificateId2'}]}
        mock_req.return_value = mockresponse
        mock_comp.side_effect = [True, False]
        self.assertEqual('certificateId1', self.cahandler._cert_id_lookup('csr_cn', 'san_list'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_024_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - two certs - 2nd match """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'subjectAltName': 'subjectAltName1', 'certificateId': 'certificateId1'}, {'subjectAltName': 'subjectAltName2', 'certificateId': 'certificateId2'}]}
        mock_req.return_value = mockresponse
        mock_comp.side_effect = [False, True]
        self.assertEqual('certificateId2', self.cahandler._cert_id_lookup('csr_cn', 'san_list'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_025_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - no certificateid in """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'subjectAltName': 'subjectAltName', 'foo': 'bar'}]}
        mock_req.return_value = mockresponse
        mock_comp.return_value = True
        self.assertFalse(self.cahandler._cert_id_lookup('csr_cn', 'san_list'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_026_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - two certs """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'subjectAltName': 'subjectAltName1', 'foo': 'bar'}, {'subjectAltName': 'subjectAltName2', 'certificateId': 'certificateId2'}]}
        mock_req.return_value = mockresponse
        mock_comp.side_effect = [True, True]
        self.assertEqual('certificateId2', self.cahandler._cert_id_lookup('csr_cn', 'san_list'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_027_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - one cert - no san in """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'foo': 'bar', 'certificateId': 'certificateId'}]}
        mock_req.return_value = mockresponse
        mock_comp.return_value = True
        self.assertFalse(self.cahandler._cert_id_lookup('csr_cn', 'san_list'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_028_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - no san_list in function """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'certificates': [{'subjectAltName': 'subjectAltName', 'certificateId': 'certificateId'}]}
        mock_req.return_value = mockresponse
        mock_comp.return_value = True
        self.assertFalse(self.cahandler._cert_id_lookup('csr_cn', None))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._san_compare')
    @patch('requests.get')
    def test_029_cert_id_lookup(self, mock_req, mock_comp):
        """ CAhandler._cert_id_lookup() - one cert - ok """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'foo': 'bar'}
        mock_req.return_value = mockresponse
        mock_comp.return_value = True
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._cert_id_lookup('csr_cn', 'san_list'))
        self.assertIn('ERROR:test_a2c:_cert_id_lookup(): no certificates found for csr_cn', lcm.output)

    @patch('requests.get')
    def test_030_cert_id_lookup(self, mock_req):
        """ CAhandler._cert_id_lookup() - request raises exception """
        self.cahandler.api_host = 'api_host'
        mock_req.side_effect = Exception('req_exc')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._cert_id_lookup('csr_cn', 'san_list'))
        self.assertIn('ERROR:test_a2c:CAhandler._cert_id_lookup() returned error: req_exc', lcm.output)

    def test_031__config_check(self):
        """ CAhandler._config.check() no api_host """
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('api_host to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"api_host" to be set in config file', lcm.output)

    def test_032__config_check(self):
        """ CAhandler._config.check() no api_user """
        self.cahandler.api_host = 'api_host'
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('api_user to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"api_user" to be set in config file', lcm.output)

    def test_033__config_check(self):
        """ CAhandler._config.check() no api_user """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': False}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('api_user to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"api_user" to be set in config file', lcm.output)

    def test_034__config_check(self):
        """ CAhandler._config.check() no api_password """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': 'api_user'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('api_password to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"api_password" to be set in config file', lcm.output)

    def test_035__config_check(self):
        """ CAhandler._config.check() no api_password """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': 'api_user', 'api_password': False}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('api_password to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"api_password" to be set in config file', lcm.output)

    def test_036__config_check(self):
        """ CAhandler._config.check() no tsg_name """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': 'api_user', 'api_password': 'api_password'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('tsg_name to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"tsg_name" to be set in config file', lcm.output)

    def test_037__config_check(self):
        """ CAhandler._config.check() no tsg_name """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': 'api_user', 'api_password': 'api_password'}
        self.cahandler.tsg_info_dic = {'name': False}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('tsg_name to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"tsg_name" to be set in config file', lcm.output)

    def test_038__config_check(self):
        """ CAhandler._config.check() no ca_name """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': 'api_user', 'api_password': 'api_password'}
        self.cahandler.tsg_info_dic = {'name': 'name'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertEqual('ca_name to be set in config file', self.cahandler.error)
        self.assertIn('ERROR:test_a2c:"ca_name" to be set in config file', lcm.output)

    def test_039__config_check(self):
        """ CAhandler._config.check() ca_bundle False """
        self.cahandler.api_host = 'api_host'
        self.cahandler.credential_dic = {'api_user': 'api_user', 'api_password': 'api_password'}
        self.cahandler.tsg_info_dic = {'name': 'name'}
        self.cahandler.ca_name = 'ca_name'
        self.cahandler.ca_id_list = ['id1', 'id2']
        self.cahandler.ca_bundle = False
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_check()
        self.assertFalse(self.cahandler.error)
        self.assertIn('WARNING:test_a2c:"ca_bundle" set to "False" - validation of server certificate disabled', lcm.output)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_040_config_load(self, mock_load_cfg):
        """ CAhandler._config_load no cahandler section """
        mock_load_cfg.return_value = {}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertTrue(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_041_config_load(self, mock_load_cfg):
        """ CAhandler._config_load api_host """
        mock_load_cfg.return_value = {'CAhandler': {'api_host': 'api_host'}}
        self.cahandler._config_load()
        self.assertEqual('api_host', self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertTrue(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_042_config_load(self, mock_load_cfg):
        """ CAhandler._config_load api_user """
        mock_load_cfg.return_value = {'CAhandler': {'api_user': 'api_user'}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': 'api_user', 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertTrue(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_043_config_load(self, mock_load_cfg):
        """ CAhandler._config_load api_password """
        mock_load_cfg.return_value = {'CAhandler': {'api_password': 'api_password'}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': 'api_password'}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertTrue(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_044_config_load(self, mock_load_cfg):
        """ CAhandler._config_load ca_name """
        mock_load_cfg.return_value = {'CAhandler': {'ca_name': 'ca_name'}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertEqual('ca_name', self.cahandler.ca_name)
        self.assertTrue(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_045_config_load(self, mock_load_cfg):
        """ CAhandler._config_load tsg_name """
        mock_load_cfg.return_value = {'CAhandler': {'tsg_name': 'tsg_name'}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': 'tsg_name', 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertTrue(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_046_config_load(self, mock_load_cfg):
        """ CAhandler._config_load ca_bundle string """
        mock_load_cfg.return_value = {'CAhandler': {'ca_bundle': 'ca_bundle'}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertEqual('ca_bundle', self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_047_config_load(self, mock_load_cfg):
        """ CAhandler._config_load ca_bundle False """
        mock_load_cfg.return_value = {'CAhandler': {'ca_bundle': False}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.load_config')
    def test_048_config_load(self, mock_load_cfg):
        """ CAhandler._config_load template_name """
        mock_load_cfg.return_value = {'CAhandler': {'template_name': 'template_name'}}
        self.cahandler._config_load()
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual({'api_user': None, 'api_password': None}, self.cahandler.credential_dic)
        self.assertEqual({'name': None, 'id': None}, self.cahandler.tsg_info_dic)
        self.assertFalse(self.cahandler.ca_name)
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_048__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts):
        """ CAhandler._csr_id_lookup - all ok """
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'subjectName': 'CN=csr_cn, O=bar', 'requestID': 'requestID'}]
        self.assertEqual('requestID', self.cahandler._csr_id_lookup('csr_cn', ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_049__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts):
        """ CAhandler._csr_id_lookup - no requestID in list """
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'subjectName': 'CN=csr_cn, O=bar'}]
        self.assertFalse(self.cahandler._csr_id_lookup('csr_cn', ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_050__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts):
        """ CAhandler._csr_id_lookup - cn in mock_unureq not correctly ordered """
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'subjectName': 'O=bar, CN=csr_cn', 'requestID': 'requestID'}]
        self.assertEqual('requestID', self.cahandler._csr_id_lookup('csr_cn', ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_051__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts):
        """ CAhandler._csr_id_lookup - empty subjectName """
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'subjectName': '', 'requestID': 'requestID'}]
        self.assertFalse(self.cahandler._csr_id_lookup('csr_cn', ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_052__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts):
        """ CAhandler._csr_id_lookup - no subjectName """
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        self.assertFalse(self.cahandler._csr_id_lookup('csr_cn', ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_053__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts):
        """ CAhandler._csr_id_lookup - requests to old """
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 100
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'subjectName': 'O=bar, CN=csr_cn', 'requestID': 'requestID'}]
        self.assertFalse(self.cahandler._csr_id_lookup('csr_cn', ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_054__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  one san """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'pkcs10': 'pkcs10', 'requestID': 'requestID'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['csr_san_list']
        self.assertEqual('requestID', self.cahandler._csr_id_lookup(None, ['csr_san_list']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_055__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  two sans """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'pkcs10': 'pkcs10', 'requestID': 'requestID'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['san1', 'san2']
        self.assertEqual('requestID', self.cahandler._csr_id_lookup(None, ['san1', 'san2']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_056__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  two sans to be reordered """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'pkcs10': 'pkcs10', 'requestID': 'requestID'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['san1', 'san2']
        self.assertEqual('requestID', self.cahandler._csr_id_lookup(None, ['san2', 'san1']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_057__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  two sans to be reordered """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'pkcs10': 'pkcs10', 'requestID': 'requestID'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['san2', 'san1']
        self.assertEqual('requestID', self.cahandler._csr_id_lookup(None, ['san1', 'san2']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_058__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  no requestID """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'pkcs10': 'pkcs10', 'foo': 'bar'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['san2', 'san1']
        self.assertFalse(self.cahandler._csr_id_lookup(None, ['san1', 'san2']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_059__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  sans are not matching """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'pkcs10': 'pkcs10', 'requestID': 'requestID'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['san1']
        self.assertFalse(self.cahandler._csr_id_lookup(None, ['san1', 'san2']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_060__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn  no pkcs10 """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mockresponse = Mock()
        mockresponse.json = lambda: [{'foo': 'bar', 'requestID': 'requestID'}]
        mock_req.return_value = mockresponse
        mock_san.return_value = ['san1']
        self.assertFalse(self.cahandler._csr_id_lookup(None, ['san1', 'san2']))

    @patch('examples.ca_handler.nclm_ca_handler.csr_san_get')
    @patch('requests.get')
    @patch('examples.ca_handler.nclm_ca_handler.date_to_uts_utc')
    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._unusedrequests_get')
    @patch('examples.ca_handler.nclm_ca_handler.uts_now')
    def test_061__csr_id_lookup(self, mock_utsnow, mock_unureq, mock_uts, mock_req, mock_san):
        """ CAhandler._csr_id_lookup - no csr_cn request throws an exception """
        self.cahandler.api_host = 'api_host'
        mock_utsnow.return_value = 1000
        mock_uts.return_value = 900
        mock_unureq.return_value = [{'addedAt': 'addedAt', 'requestID': 'requestID'}]
        mock_req.side_effect = Exception('exc_csr_id_lookup')
        mock_san.return_value = ['san1']
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._csr_id_lookup(None, ['san1', 'san2']))
        self.assertIn('ERROR:test_a2c:CAhandler._csr_id_lookup() returned error: exc_csr_id_lookup', lcm.output)

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._api_post')
    def test_062__request_import(self, mock_req):
        """ CAhandler._request_import """
        self.cahandler.api_host = 'api_host'
        mock_req.return_value = 'foo'
        self.assertEqual('foo', self.cahandler._request_import('csr'))

    @patch('examples.ca_handler.nclm_ca_handler.CAhandler._api_post')
    def test_063__request_import(self, mock_req):
        """ CAhandler._request_import - req raises an exception """
        self.cahandler.api_host = 'api_host'
        mock_req.side_effect = Exception('exc_req_import')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._request_import('csr'))
        self.assertIn('ERROR:test_a2c:CAhandler._request_import() returned error: exc_req_import', lcm.output)

    @patch('requests.get')
    def test_064__unusedrequests_get(self, mock_req):
        """ CAhandler._unusedrequests_get """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'foo': 'bar'}
        mock_req.return_value = mockresponse
        self.assertEqual({'foo': 'bar'}, self.cahandler._unusedrequests_get())

    @patch('requests.get')
    def test_065__unusedrequests_get(self, mock_req):
        """ CAhandler._unusedrequests_get """
        self.cahandler.api_host = 'api_host'
        mock_req.side_effect = Exception('exc_req_unused')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._unusedrequests_get())
        self.assertIn('ERROR:test_a2c:CAhandler._unusedrequests_get() returned error: exc_req_unused', lcm.output)

    @patch('requests.post')
    @patch('requests.get')
    def test_066__login(self, mock_get, mock_post):
        """ CAhandler._unusedrequests_get """
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.status_code = lambda: 'foo'
        mock_get.return_value = mockresponse1
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'access_token': 'access_token', 'username': 'username', 'realms': 'realms'}
        mock_post.return_value = mockresponse2
        self.cahandler._login()
        self.assertEqual({'Authorization': 'Bearer access_token'}, self.cahandler.headers)

    @patch('requests.post')
    @patch('requests.get')
    def test_067__login(self, mock_get, mock_post):
        """ CAhandler._unusedrequests_get  mock_post without username"""
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.status_code = lambda: 'foo'
        mock_get.return_value = mockresponse1
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'access_token': 'access_token', 'foo': 'bar', 'realms': 'realms'}
        mock_post.return_value = mockresponse2
        self.cahandler._login()
        self.assertEqual({'Authorization': 'Bearer access_token'}, self.cahandler.headers)

    @patch('requests.post')
    @patch('requests.get')
    def test_068__login(self, mock_get, mock_post):
        """ CAhandler._unusedrequests_get mock_post without realms"""
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.status_code = lambda: 'foo'
        mock_get.return_value = mockresponse1
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'access_token': 'access_token', 'username': 'username', 'foo': 'bar'}
        mock_post.return_value = mockresponse2
        self.cahandler._login()
        self.assertEqual({'Authorization': 'Bearer access_token'}, self.cahandler.headers)

    @patch('requests.post')
    @patch('requests.get')
    def test_069__login(self, mock_get, mock_post):
        """ CAhandler._unusedrequests_get mock_post without access tooken"""
        self.cahandler.api_host = 'api_host'
        mockresponse1 = Mock()
        mockresponse1.status_code = lambda: 'foo'
        mockresponse1.ok = 'ok'
        mock_get.return_value = mockresponse1
        mockresponse2 = Mock()
        mockresponse2.json = lambda: {'foo': 'bar', 'username': 'username', 'realms': 'realms'}
        mock_post.return_value = mockresponse2
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._login()
        self.assertFalse(self.cahandler.headers)
        self.assertIn('ERROR:test_a2c:CAhandler._login(): No token returned. Aborting...', lcm.output)

    def test_070__san_compare(self):
        """ CAhandler._san_compare all ok """
        csr_san_list = ['foo:foo']
        cert_san_list = {'foo': ['foo']}
        self.assertTrue(self.cahandler._san_compare(csr_san_list, cert_san_list))

    def test_071__san_compare(self):
        """ CAhandler._san_compare multiple """
        csr_san_list = ['foo:foo', 'foo:bar']
        cert_san_list = {'foo': ['foo', 'bar']}
        self.assertTrue(self.cahandler._san_compare(csr_san_list, cert_san_list))

    def test_072__san_compare(self):
        """ CAhandler._san_compare multiple """
        csr_san_list = ['foo:foo,foo:bar']
        cert_san_list = {'foo': ['foo', 'bar']}
        self.assertTrue(self.cahandler._san_compare(csr_san_list, cert_san_list))

    def test_073__san_compare(self):
        """ CAhandler._san_compare multiple """
        csr_san_list = ['foo:foo,foo:bar1']
        cert_san_list = {'foo': ['foo', 'bar']}
        self.assertFalse(self.cahandler._san_compare(csr_san_list, cert_san_list))

    def test_074_poll(self):
        """ CAhandler.poll() """
        self.assertEqual(('Method not implemented.', None, None, 'poll_identifier', False), self.cahandler.poll('cert_name', 'poll_identifier', 'csr'))

    def test_075_trigger(self):
        """ CAhandler.trigger() """
        self.assertEqual(('Method not implemented.', None, None), self.cahandler.trigger('payload'))

    @patch('requests.get')
    def test_076___tsg_id_lookup(self, mock_get):
        """ CAhandler._tsg_id_lookup() - all ok """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'targetSystemGroups': [{'name': 'name', 'id': 'id'}]}
        mock_get.return_value = mockresponse
        self.cahandler.tsg_info_dic = {'name': 'name', 'id': None}
        self.cahandler._tsg_id_lookup()
        self.assertEqual({'name': 'name', 'id': 'id'}, self.cahandler.tsg_info_dic)

    @patch('requests.get')
    def test_077___tsg_id_lookup(self, mock_get):
        """ CAhandler._tsg_id_lookup() - multipe returned 1st matches """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'targetSystemGroups': [{'name': 'name', 'id': 'id'}, {'name': 'name1', 'id': 'id1'}]}
        mock_get.return_value = mockresponse
        self.cahandler.tsg_info_dic = {'name': 'name', 'id': None}
        self.cahandler._tsg_id_lookup()
        self.assertEqual({'name': 'name', 'id': 'id'}, self.cahandler.tsg_info_dic)

    @patch('requests.get')
    def test_078___tsg_id_lookup(self, mock_get):
        """ CAhandler._tsg_id_lookup() - multipe returned 2nd matches """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'targetSystemGroups': [{'name': 'name1', 'id': 'id1'}, {'name': 'name', 'id': 'id'}]}
        mock_get.return_value = mockresponse
        self.cahandler.tsg_info_dic = {'name': 'name', 'id': None}
        self.cahandler._tsg_id_lookup()
        self.assertEqual({'name': 'name', 'id': 'id'}, self.cahandler.tsg_info_dic)

    @patch('requests.get')
    def test_079___tsg_id_lookup(self, mock_get):
        """ CAhandler._tsg_id_lookup() - id is missing """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'targetSystemGroups': [{'name': 'name'}]}
        mock_get.return_value = mockresponse
        self.cahandler.tsg_info_dic = {'name': 'name', 'id': None}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._tsg_id_lookup()
        self.assertEqual({'name': 'name', 'id': None}, self.cahandler.tsg_info_dic)
        self.assertIn("ERROR:test_a2c:CAhandler._tsg_id_lookup() incomplete response: {'name': 'name'}", lcm.output)

    @patch('requests.get')
    def test_080___tsg_id_lookup(self, mock_get):
        """ CAhandler._tsg_id_lookup() - name is missing """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'targetSystemGroups': [{'foo': 'bar', 'id': 'id'}]}
        mock_get.return_value = mockresponse
        self.cahandler.tsg_info_dic = {'name': 'name', 'id': None}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._tsg_id_lookup()
        self.assertEqual({'name': 'name', 'id': None}, self.cahandler.tsg_info_dic)
        self.assertIn("ERROR:test_a2c:CAhandler._tsg_id_lookup() incomplete response: {'foo': 'bar', 'id': 'id'}", lcm.output)

    @patch('requests.get')
    def test_081___tsg_id_lookup(self, mock_get):
        """ CAhandler._tsg_id_lookup() - targetSystemGroups is missing """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'tsg': [{'foo': 'bar', 'id': 'id'}]}
        mock_get.return_value = mockresponse
        self.cahandler.tsg_info_dic = {'name': 'name', 'id': None}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._tsg_id_lookup()
        self.assertEqual({'name': 'name', 'id': None}, self.cahandler.tsg_info_dic)
        self.assertIn('ERROR:test_a2c:CAhandler._tsg_id_lookup() no target-system-groups found for filter: name...', lcm.output)

    @patch('requests.get')
    def test_082__tsg_id_lookup(self, mock_req):
        """ CAhandler._request_import - req raises an exception """
        self.cahandler.api_host = 'api_host'
        mock_req.side_effect = Exception('exc_tsg_id_lookup')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertFalse(self.cahandler._tsg_id_lookup())
        self.assertIn('ERROR:test_a2c:CAhandler._tsg_id_lookup() returned error: exc_tsg_id_lookup', lcm.output)

    @patch('requests.get')
    def test_083__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - all ok """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': True, 'linkId': 10, 'linkType': 'TEMPLATE'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': 10}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_084__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - linkId None """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': True, 'linkId': None, 'linkType': 'TEMPLATE'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_085__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - No linkId """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': True, 'linkType': 'TEMPLATE'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_086__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - no match in template names """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'nomatch', 'allowed': True, 'linkId': 10, 'linkType': 'TEMPLATE'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_088__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - allowed false """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': False, 'linkId': 10, 'linkType': 'TEMPLATE'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_089__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - template in lower cases """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': True, 'linkId': 10, 'linkType': 'template'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': 10}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_090__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - no template """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': True, 'linkId': 10, 'linkType': 'linkType'}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_091__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - no linktype """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': [{'displayName': 'template_name', 'allowed': True, 'linkId': 10}]}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_092__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - empty list """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'items': []}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_093__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - no items """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'template': {'blank': []}}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_094__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - wrong dict """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'foo': 'bar'}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_095__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - wrong dict """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = lambda: {'foo': 'bar'}
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_096__template_id_lookup(self, mock_get):
        """ CAhandler._template_id_lookup() - empty response """
        self.cahandler.api_host = 'api_host'
        mockresponse = Mock()
        mockresponse.json = None
        mock_get.return_value = mockresponse
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)

    @patch('requests.get')
    def test_097__template_id_lookup(self, mock_req):
        """ CAhandler._cert_id_lookup() - request raises exception """
        self.cahandler.api_host = 'api_host'
        mock_req.side_effect = Exception('req_exc')
        self.cahandler.template_info_dic = {'name': 'template_name', 'id': None}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._template_id_lookup()
        self.assertEqual({'name': 'template_name', 'id': None}, self.cahandler.template_info_dic)
        self.assertIn('ERROR:test_a2c:CAhandler._template_id_lookup() returned error: req_exc', lcm.output)

if __name__ == '__main__':

    if os.path.exists('acme_test.db'):
        os.remove('acme_test.db')
    unittest.main()
