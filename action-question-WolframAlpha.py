#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import io
import ConfigParser

from omniscient import Omniscient
from hermes_python.hermes import Hermes
from hermes_python.ontology import *

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    #conf = read_configuration_file(CONFIG_INI)
    message = omniscient.get_answer(intentMessage.input)
    print('end session: ' + message)
    hermes.publish_end_session(intentMessage.session_id, message)


if __name__ == "__main__":
    config = read_configuration_file(CONFIG_INI)   
    omniscient = Omniscient(config)
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("RumoOr:question", subscribe_intent_callback).start()