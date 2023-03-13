import os
import logging
import argparse

from pytryfi import PyTryFi

parser=argparse.ArgumentParser()

if 'fi_user' in os.environ:
    username = { 'default': os.environ['fi_user'] }
else:
    username = { 'required': True, }
parser.add_argument(
    "-u", "--username", help="Provide username for Fi Collar",
    **username)

if 'fi_pass' in os.environ:
    password = { 'default': os.environ['fi_pass'] }
else:
    password = { 'required': True }
parser.add_argument(
    "-p", "--password", help="Provide password for Fi Collar",
    **password)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

tryfi = PyTryFi(args.username, args.password)

print(tryfi)
