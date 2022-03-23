#!/usr/bin/env python

"""
Project: PayPal Tracking ID

Description: updates the shipping information for a particular PayPal transaction

"""
__author__ = "Guido Boehm"
__projectname__ = "PayPal-Tracking-ID"
__filename__ = "pp_tracking_id.py"
__credits__ = [""]
__license__ = "see LICENSE file"
__version__ = "0.0.2"
__maintainer__ = "Guido Boehm"
__email__ = "olb@family-boehm.de"
__status__ = "Prototype"
__copyright__ = """
Copyright 2022, Guido Boehm
All Rights Reserved. 
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE. 
"""

from Classes import ParseKwargs, PayPalAPI

import argparse

import sys
import yaml

from pathlib import Path


def write_error_log(directory, filename, message):
    """write_error_log

    this function writes an error log to local disk

    :param directory: string: direactory name
    :param filename: string: filename
    :param message: str: message that is written to the file
    :return:
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    filename = Path(directory, filename + '.txt')
    with filename.open('a', encoding='utf-8') as file:
        file.write(message)


def main(args=None):
    """main

    main function fo the script
    :param args:
    :return:
    """
    ###########################################################################
    # read parameters from yaml file
    ###########################################################################
    config_file = Path('./config.yaml')
    with config_file.open('r') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config = yaml.full_load(file)

    api = 'LiveAPI' if config['LiveModus'] else 'SandBoxAPI'
    credentials = 'CredentialsLive' if config['LiveModus'] else 'CredentialsSandBox'

    PayPalAPI.baseurl = config[api]['BaseUrl']
    PayPalAPI.debug = config['Debug']
    paypal = PayPalAPI(client_id=config[credentials]['Client_ID'], secret=config[credentials]['Secret'])
    try:
        paypal.get_token(config[api]['EndPoint_Token'])
    except Exception as err:
        write_error_log('./failed-trasactions', args['shipping_details']['transaction_id'], str(err))

    args['shipping_details'].update({'EndPoint_TrackersBatch': config['LiveAPI']['EndPoint_TrackersBatch'] if config[
        'LiveModus'] else config['SandBoxAPI']['EndPoint_TrackersBatch']})

    try:
        paypal.set_shipping_status(**args['shipping_details'])
    except Exception as err:
        write_error_log('./failed-trasactions', args['shipping_details']['transaction_id'], 'Errormessage: ' + str(
                err) + '\n')

    if paypal.debug_message:
        write_error_log('./failed-trasactions', args['shipping_details']['transaction_id'], paypal.debug_message)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
            description="Diese Skript setzt den Sendungsstatus (Tracking ID, Sendungsstatus) für eine bestimmte "
                        "PayPal Transaktion"
    )
    req_args = arg_parser.add_argument_group(title='required arguments')
    req_args.add_argument(
            "--parameter", "-p", nargs='*',
            action=ParseKwargs,
            dest="parameters",
            help="bitte Sendungsparaneter angeben"
    )

    input_args = {}
    if len(sys.argv) > 1:
        usr_input = arg_parser.parse_args()

    else:
        arg_parser.print_help()
        sys.exit()
    input_args['shipping_details'] = usr_input.parameters

    main(input_args)
