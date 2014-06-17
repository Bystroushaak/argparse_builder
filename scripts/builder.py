# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
import animator


# Variables ===================================================================
ARG_PARSER_TEMPLATE = """import argparse

# ...
parser = argparse.ArgumentParser(
    $parameters
)
$arguments
args = parser.parser_args()

"""

ARG_TEMPLATE = """parser.add_argument(
    $parameters
)"""


# Functions & objects =========================================================
def _filtered_dict(d):
    return dict(
        filter(
            lambda x: not x[0].startswith("_"),
            d.items()
        )
    )


def _dict_to_params(d, non_str):
    out = []
    for key, val in d.items():
        if val is None:
            continue

        val = str(val)
        line = str(key) + "="

        if key in non_str:
            line += val
        else:
            val = val.replace(r"\\", r"\\")
            quote = '"'
            if "\n" in val:
                quote = quote * 3
            line += quote + val + quote

        out.append(line)

    return out


class ArgumentParser(object):
    def __init__(self):
        self.prog = None
        self.usage = None
        self.description = None
        self.epilog = None
        self.add_help = None

        self._non_str = [
            "prog",
            "add_help"
        ]

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

            if item.type == "checkbox":
                value = item.checked

            self.__setattr__(key, value)

    def __str__(self):
        return ARG_PARSER_TEMPLATE.replace(
            "$parameters",
            ",\n    ".join(_dict_to_params(self.get_dict(), self._non_str))
        )


class Argument(object):
    def __init__(self, element):
        tag_pool = ["input", "textarea", "select"]
        self._arguments = sum(
            map(lambda x: element.get(selector=x), tag_pool),
            []
        )

        self._non_str = [
            "const",
            "default",
            "type",
            "choices",
            "required"
        ]

    def update(self):
        # read dynamically all arguments
        for item in self._arguments:
            value = item.value

            # default values == None
            if value == item.title or value.strip() == "":
                value = None

            if item.type == "checkbox":
                value = item.checked

            self.__setattr__(item.id.split("_")[-1], value)

    def get_dict(self):
        self.update()
        return _filtered_dict(self.__dict__)

    def __str__(self):
        return ARG_TEMPLATE.replace(
            "$parameters",
            ",\n    ".join(_dict_to_params(self.get_dict(), self._non_str))
        )


class Argparse:
    def __init__(self):
        self.argparse = ArgumentParser()
        self.arguments = []

    def update(self):
        self.argparse.update()

        self.arguments = list(map(lambda x: Argument(x), animator.get_list_of_arguments()))

    def __str__(self, ev=None):
        self.update()

        # return str(self.argparse) + "\n" + str(list(map(lambda x: x.get_dict(), self.arguments)))
        return str(self.argparse).replace(
            "$arguments",
            "\n".join(list(map(lambda x: str(x), self.arguments)))
        )


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
