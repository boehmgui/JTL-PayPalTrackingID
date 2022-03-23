
import argparse
import json
import requests

from datetime import datetime


class RESOURCE_NOT_FOUND(Exception):
    pass


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


class PayPalAPI:
    """PayPalAPI

    implments some methods of PayPal's Tackers batch resource group described at https://developer.paypal.com/api/tracking/v1/#trackers-batch_post
    """
    baseurl: str = 'https://api-m.sandbox.paypal.com'
    debug: bool = False

    def __init__(self, client_id: str, secret: str):
        """__init__

        initializes an instance of the PayPal class; sets client id and secret, which are required by some methods
        Generation of the credentials is described here: https://developer.paypal.com/api/rest/#link-getcredentials

        :param client_id: client id (str)
        :param secret: secret (str)
        """
        self.client_id = client_id
        self.secret = secret
        self._token = None
        self._debug_message = ''

    @property
    def client_id(self):
        """client_id

        returns the client id that is required for API authentication
        :return:
        """
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        """client_id

        setter function for the client id that is required for API authentication
        :return:
        """
        if not isinstance(value, str):
            raise ValueError('client ID must be a string')
        value = value.strip()
        if not value:
            raise ValueError('client ID cannot be empty')
        self._client_id = value

    @property
    def secret(self):
        """secret

        returns the secret that is required for API authentication
        :return:
        """
        return self._secret

    @secret.setter
    def secret(self, value):
        """secret

        setter function for the secret that is required for API authentication
        :return:
        """
        if not isinstance(value, str):
            raise ValueError('secret must be a string')
        value = value.strip()
        if not value:
            raise ValueError('secret cannot be empty')
        self._secret = value

    @property
    def token(self):
        """token

        returns the token that is required for API authentication
        :return:
        """
        return self._token

    def get_token(self, endpoint):
        """get_token

        obtans the authentication token from PayPal API
        :return:
        """
        url = PayPalAPI.baseurl + endpoint
        payload = 'grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request(method='POST', url=url, auth=(self.client_id, self.secret), headers=headers,
                                    data=payload)
        if PayPalAPI.debug:
            self.debug_message = f"Method:{self.set_shipping_status.__name__}\n"
            self.debug_message = f"url={url}\n"
            self.debug_message = f"headers={headers}\n"
            self.debug_message = f"payload={payload}\n\n"

        if response.ok:
            self._token = response.json()['access_token']
        else:
            response.raise_for_status()

    def set_shipping_status(self, **kwargs):
        """
        sets the shipping status for a particular transaction ID
        # https://developer.paypal.com/api/tracking/v1/#definition-tracker

        :param kwargs:
                transaction_id: string - required
                tracking_number: string - optional
                status: enum - required
                shipment_date: string - optional (current date/time if missing)
                carrier: enum -  (set to OTHER if carrier name is not in list of Carriers at https://developer.paypal.com/docs/tracking/reference/carriers/)
                carrier_name_other: string (carrier name if carrier is set to OTHER)
        :return:
        """

        try:
            transaction_id = kwargs['transaction_id']
        except KeyError as err:
            raise ValueError from err

        shipment_date = kwargs.get('shipment_date', datetime.now().date().isoformat())
        tracking_number = kwargs.get('tracking_number', '')
        status = kwargs.get('status', 'SHIPPED')
        carrier = kwargs.get('carrier', 'OTHER')
        carrier_name_other = kwargs.get('carrier_name_other', 'other')

        url = PayPalAPI.baseurl + kwargs['EndPoint_TrackersBatch']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        payload = {
            'trackers': [
                {
                    'transaction_id': transaction_id,
                    'status': status.upper(),
                    'shipment_date': shipment_date
                }
            ]
        }

        # add the carrier to the payload
        carrier = carrier.upper()
        if tracking_number:
            payload['trackers'][0].update({'tracking_number': tracking_number})

            # only if tracking number is provided we can set the carrier id
            if carrier != 'OTHER':
                payload['trackers'][0].update({'carrier': carrier})
            else:
                payload['trackers'][0].update({'carrier': carrier})
                payload['trackers'][0].update({'carrier_name_other': carrier_name_other})

        payload = json.dumps(payload)

        response = requests.request(method='POST', url=url, headers=headers, data=payload)
        if PayPalAPI.debug:
            self.debug_message = f"Method:{self.set_shipping_status.__name__}\n"
            self.debug_message = f"parameters{kwargs}\n"
            self.debug_message = f"url={url}\n"
            self.debug_message = f"headers={headers}\n"
            self.debug_message = f"payload={payload}\n\n"

        if response.ok:
            text = response.json()
            if text['errors']:
                error = text['errors'][0]
                raise RESOURCE_NOT_FOUND(f"{error['name']}: {error['message']} - {error['details']}")
            else:
                response.raise_for_status()

    @property
    def debug_message(self):
        return self._debug_message

    @debug_message.setter
    def debug_message(self, value):
        self._debug_message += str(value)


def main(args=None):
    pass


if __name__ == "__main__":

    main()
