
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from tony_util.dir_diagnostics import values
import pprint
pp = pprint.PrettyPrinter(indent=4)  # usage pp.pprint(stuff)


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
