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
class ArgumentCommon(object):
    def __init__(self, ):
        self._non_str = []
        self._template = ""

    def _filtered_dict(self):
        return dict(
            filter(
                lambda x: not x[0].startswith("_"),
                self.__dict__.items()
            )
        )

    def _dict_to_params(self):
        out = []
        for key, val in self._filtered_dict().items():
            if val is None :
                continue

            line = str(key) + "="
            val = str(val)

            # don't escape native values
            if key in self._non_str:
                line += val
            else:
                val = val.replace(r"\\", r"\\")

                # handle multiline strings
                quote = '"'
                if "\n" in val:
                    quote = quote * 3

                line += quote + val + quote

            out.append(line)

        return out

    def __str__(self):
        params = self._dict_to_params()

        if not params:
            return ""

        return self._template.replace(
            "$parameters",
            ",\n    ".join(params)
        )


class ArgumentParser(ArgumentCommon):
    def __init__(self):
        self.prog = None
        self.usage = None
        self.description = None
        self.epilog = None
        self.add_help = None

        # don't quote following parameters;
        self._non_str = [
            "prog",
            "add_help"
        ]

        self._prefix = "ArgumentParser_"
        self._template = ARG_PARSER_TEMPLATE

    def get_dict(self):
        return self._filtered_dict()

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


class Argument(ArgumentCommon):
    def __init__(self, element):
        tag_pool = ["input", "textarea", "select"]
        self._arguments = sum(
            map(lambda x: element.get(selector=x), tag_pool),
            []
        )

        # don't quote following parameters;
        self._non_str = [
            "const",
            "default",
            "type",
            "choices",
            "required",
            "nargs"
        ]

        self._non_str_defaults = {
            "type": "str",
            "action": "store",
            "required": False
        }

        self._template = ARG_TEMPLATE

    def update(self):
        # read dynamically all arguments
        for item in self._arguments:
            value = item.value
            arg_name = item.id.split("_")[-1]

            # default values == None
            if value == item.title or value.strip() == "":
                value = None

            if item.type == "checkbox":
                value = item.checked

            if self._non_str_defaults.get(arg_name, False) == value:
                value = None

            self.__setattr__(arg_name, value)

    def _filtered_dict(self):
        self.update()
        return super(Argument, self)._filtered_dict()


class Argparse:  # TODO: check how many times is update called
    def __init__(self):
        self.argparse = ArgumentParser()
        self.arguments = []

    def update(self):
        self.argparse.update()

        self.arguments = map(
            lambda x: Argument(x),
            animator.get_list_of_arguments()
        )

    def __str__(self, ev=None):
        self.update()

        return str(self.argparse).replace(
            "$arguments",
            "\n".join(map(lambda x: str(x), self.arguments))
        )


# Main program ================================================================
a = Argparse()

def set_txt(ev=None):
    doc["output"].value = a.__str__()

doc["output"].bind("click", set_txt)
