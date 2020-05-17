#!/usr/bin/python
""" database updater """
import sys
sys.path.insert(0, '..')
from acme.helper import logger_setup
from acme.certificate import Certificate


if __name__ == '__main__':

    DEBUG = True
    # initialize logger
    LOGGER = logger_setup(DEBUG)

    with Certificate(DEBUG, 'foo', LOGGER) as certificate:
        # search certificates in status "processing"
        CERT_LIST = certificate.certlist_search('order__status_id', 4, ('name', 'poll_identifier', 'csr'))

        from pprint import pprint
        pprint(CERT_LIST)
