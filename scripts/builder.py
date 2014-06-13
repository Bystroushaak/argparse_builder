# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
from browser import html


# Variables ===================================================================
# Functions & objects =========================================================
class ArgumentParserConf(object):
    def __init__(self):
        self.prog = None
        self.usage = None
        self.description = None
        self.epilog = None
        self.add_help = None

        self._prefix = "ArgumentParser_"

    def get_dict(self):
        return dict(
            filter(
                lambda x: not x[0].startswith("_"),
                self.__dict__.items()
            )
        )

    def update(self):
        for key in self.get_dict().keys():
            self.__setattr__(
                key,
                doc[self._prefix + key].value
            )

    def get_ids(self):
        return map(lambda x: self._prefix + x, self.get_dict().keys())


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


def defaults_to_values():
    for key in doc[html.INPUT] + doc[html.TEXTAREA]:
        # skip already filled values
        if key.value.strip():
            continue

        if key.type == "text" or key.nodeName == "TEXTAREA":
            key.value = key.title


# Main program ================================================================
