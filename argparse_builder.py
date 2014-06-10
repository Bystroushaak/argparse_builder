#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc


# Variables ===================================================================



# Functions & objects =========================================================



# Main program ================================================================
class ArgumentParserConf(object):
    def __init__(self):
        self.prog = None
        self.usage = None
        self.description = None
        self.epilog = None
        self.add_help = None

    def update_data(self):
        for key in self.__dict__.keys():
            if key.startswith("_"):
                continue

            self.__setattr__(
                key,
                doc["ArgumentParser_" + key].value
            )

    def get_dict(self):
        return dict(
            filter(
                lambda x: not x[0].startswith("_"),
                self.__dict__.items()
            )
        )


class Argument:
    def __init__(self, element_id):
        pass


class Argparse:
    def __init__(self):
        self.argparse = ArgumentParserConf()
        self.arguments = []


a = ArgumentParserConf()
a.update_data()
doc["output"] <= str(a.get_dict())


def serialize_to_python(args):
    """
    Serializes dictionary with data to actual python code, which is then
    displayed in output textarea.
    """
    pass

def collect_data():
    """
    Collects data from all forms to the Configuration object.
    """
    pass