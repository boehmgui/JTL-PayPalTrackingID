"""
Project: PayPal-Tracking-ID
Filename: ${FILE_NAME}
Description

"""
__author__ = "Guido Boehm"
__copyright__ = "Copyright 2022, PayPal-Tracking-ID"
__filename__ = "${FILE_NAME}"
__credits__ = [""]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Guido Boehm"
__email__ = "guido@family-boehm.de"
__status__ = "Prototype"

from src.Classes import PayPalAPI

import json
import os
import requests
import requests_mock

from pathlib import Path
from unittest import TestCase

SCRIPT_PATH = Path(__file__).parent.absolute()
DATA_DIR = Path(SCRIPT_PATH, 'data')


class TestPayPalAPI(TestCase):

    @requests_mock.mock()
    def test_get_token_success(self, mock):
        paypal = PayPalAPI(client_id='abc', secret='123')
        url = PayPalAPI.baseurl + '/v1/oauth2/token'
        filename = Path(DATA_DIR, "token_success.json")
        with filename.open('r') as file:
            response = json.load(file)
        mock.post(url, json=response, status_code=200)
        paypal.get_token('/v1/oauth2/token')
        self.assertEqual(paypal.token, response['access_token'])

    @requests_mock.mock()
    def test_get_token_auth_failed(self, mock):
        paypal = PayPalAPI(client_id='abc', secret='123')
        url = PayPalAPI.baseurl + '/v1/oauth2/token'
        filename = Path(DATA_DIR, "token_auth_failed.json")
        with filename.open('r') as file:
            response = json.load(file)
        mock.post(url, json=response, status_code=401)
        with self.assertRaises(requests.exceptions.HTTPError):
            paypal.get_token('/v1/oauth2/token')

    @requests_mock.mock()
    def test_set_shipping_status(self, mock):
        paypal = PayPalAPI(client_id='abc', secret='123')
        url = PayPalAPI.baseurl + '/v1/shipping/trackers-batch'
        self.skipTest('not implemented')

    def test_client_id(self):
        paypal = PayPalAPI(client_id='abc', secret='123')
        self.assertEqual(paypal.client_id, 'abc')
        self.assertEqual(paypal.secret, '123')
        with self.assertRaises(ValueError):
            paypal.client_id = 123
        with self.assertRaises(ValueError):
            paypal.client_id = ' '
        with self.assertRaises(ValueError):
            paypal.secret = 123
        with self.assertRaises(ValueError):
            paypal.secret = ' '


def main(args=None):
    pass


if __name__ == "__main__":

    main()
