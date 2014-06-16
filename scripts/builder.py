# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
import animator


# Variables ===================================================================
# Functions & objects =========================================================
def _filtered_dict(d):
    return dict(
        filter(
            lambda x: not x[0].startswith("_"),
            d.items()
        )
    )


class ArgumentParserConf(object):
    def __init__(self):
        self.prog = None
        self.usage = None
        self.description = None
        self.epilog = None
        self.add_help = None

        self._prefix = "ArgumentParser_"

    def get_dict(self):
        return _filtered_dict(self.__dict__)

    def update(self):
        for key in self.get_dict().keys():
            item = doc[self._prefix + key]
            value = item.value

            # default values == None
            if value == item.title or value.strip() == "":
                value = None

            self.__setattr__(key, value)

    # def get_ids(self):
        # return map(lambda x: self._prefix + x, self.get_dict().keys())


class Argument(object):
    def __init__(self, element):
        tag_pool = ["input", "textarea", "select"]
        self._arguments = sum(
            map(lambda x: element.get(selector=x), tag_pool),
            []
        )

        self.update()

    def update(self):
        # read dynamically all arguments
        for item in self._arguments:
            value = item.value

            # default values == None
            if value == item.title or value.strip() == "":
                value = None

            self.__setattr__(item.id.split("_")[-1], value)

    def get_dict(self):
        return _filtered_dict(self.__dict__)


class Argparse:
    def __init__(self):
        self.argparse = ArgumentParserConf()
        self.arguments = []

        self.update()

    def update(self):
        self.argparse.update()

        self.arguments = list(map(lambda x: Argument(x), animator.get_list_of_arguments()))

    def __str__(self, ev=None):
        return str(self.argparse.get_dict()) + "\n" + str(list(map(lambda x: x.get_dict(), self.arguments)))
        # 
        # return str(Argument(animator.get_list_of_arguments()[0]).__dict__)


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


# Main program ================================================================
a = Argparse()

def set_txt(ev=None):
    doc["output"].value = a.__str__()

doc["output"].bind("click", set_txt)
