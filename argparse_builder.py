#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
from browser.local_storage import storage


# Variables ===================================================================
_VER = 0.1


# Functions & objects =========================================================



# Main program ================================================================
class ArgumentParserConf(object):
    def __init__(self):
        self.prog = None
        self.usage = None
        self.description = None
        self.epilog = None
        self.add_help = None

    def update(self):
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

        self.update()

    def update(self):
        self.argparse.update()


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


# save default values of each imput when first run
if "_DEF" not in storage or "_VER" not in storage or storage["_VER"] != _VER:
    storage["_DEF"] = Argparse()
    storage["_VER"] = _VER

doc["output"] <= str(storage["_VER"])