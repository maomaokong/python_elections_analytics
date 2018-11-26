import os
import json


class Config:
    """
    Read default configurations from setting file
    """
    PATH_PARENT = os.path.dirname(os.getcwd())

    config_file = '{pp}/config.json'.format(pp=PATH_PARENT)

    with open(config_file, 'r') as cf:
        config = json.load(cf)

        APP_NAME = config['APP_NAME']
        VERSION = config['VERSION']
        ENV = config['ENV']

        PATH_SRC = config['PATHS']['SOURCE_CODE']
        PATH_DATA = config['PATHS']['DATA']
        PATH_DATA_INPUT = config['PATHS']['DATA_INPUT']
        PATH_DATA_OUTPUT = config['PATHS']['DATA_OUTPUT']
        PATH_LOG = config['PATHS']['LOG']
        PATH_TEST = config['PATHS']['TEST']
        PATH_DB = config['PATHS']['DB']

        INPUT_ELECTIONS = config['INPUT']['ELECTION_DATA']

        DB_FILENAME = config['DB']['FILENAME']

        DB_QUERY_01 = config['DB']['CREATE_TBL_QUERY_01']


class Environment:
    """
    Environment Value
    """
    UAT = 1
    PROD = 9
