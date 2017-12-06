import json
import logging.config


class Logger(object):

    def __init__(self, config_file):

        self.config_file = config_file

    def genLogger(self, logger_name):

        with open(self.config_file, "rt") as logconf:

            config = json.load(logconf)

        logging.config.dictConfig(config)

        return logging.getLogger(logger_name)

    @classmethod
    def win_logger(cls):

        return cls("config/server_log_config.json")

    @classmethod
    def client_logger(cls):

        return cls("config/client_log_config.json")
