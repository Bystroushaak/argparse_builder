# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import html
from browser import document as doc

from collections import OrderedDict

# import animator
import argtools


# Variables ===================================================================
ARG_PARSER_TEMPLATE = """import argparse

# ...
parser = argparse.ArgumentParser(
    $parameters
)
$arguments
args = parser.parse_args()

"""

ARG_TEMPLATE = """parser.add_argument(
    $parameters
)"""


# Functions & objects =========================================================
class ArgInput(object):
    def __init__(self, element):
        self.ID = element.id.split("_")[0]
        self.name = element.id.split("_")[-1]
        self.element = element

        if self.element.value == "":
            self.element.value = self.element.title

        def input_remove_help(ev):
            if ev.target.value == ev.target.title:
                ev.target.value = ""

        def input_add_help(ev):
            if ev.target.value == "":
                ev.target.value = ev.target.title

        self.is_text_type = (element.type == "text" or element.nodeName == "TEXTAREA")

        if self.is_text_type:
            element.bind("focus", input_remove_help)
            element.bind("blur", input_add_help)

    @property
    def value(self):
        # selects
        if not self.is_text_type and \
           self.element.value == self.element._default:
            return None

        if self.element.type == "checkbox":
            value = self.element.checked

            if self.element._default == str(value):
                return None

            return value

        if self.element.value != self.element.title:
            if self.element._non_str:
                return self.element.value

            return '"' + self.element.value + '"'  # TODO: long lines / mutiple lines

        return None

    @value.setter
    def value(self, new_val):
        self.element.value = new_val

    def __str__(self):
        if self.element._non_key:
            return str(self.value)

        return self.name + "=" + str(self.value)


class Argument(object):
    def __init__(self):
        self.ID = str(argtools.get_id_from_pool())
        element = self._add_html_repr()

        arguments = element.get(selector="input")
        arguments = list(filter(lambda x: x.type != "button", arguments))
        arguments += element.get(selector="select")
        arguments += element.get(selector="textarea")
        self.inputs = OrderedDict(
            map(
                lambda x: (x.id.split("_")[-1], ArgInput(x)),
                sum(arguments, [])
            )
        )

        self._non_str_defaults = {
            "type": "str",
            "action": "store",
            "required": False
        }

    def _add_html_repr(self):
        """
        Add new argument table.
        """
        template = doc["argument_template"].innerHTML

        table = html.TABLE(id=self.ID + "_argument", Class="argument_table")
        table.html = template.replace("$ID", self.ID)
        doc["arguments"] <= table

        # add_callbacks(ID)
        return table

    def remove(self):
        doc[self.ID + "_argument"].outerHTML = ""

    def __str__(self):
        vals = map(
            lambda x: str(x),
            filter(
                lambda x: x.value is not None,
                self.inputs.values()
            )
        )

        if len(list(vals)) == 0:
            return ""

        return ARG_TEMPLATE.replace(
            "$parameters",
            "\t" + "\n\t".join(vals)
        )





# Main program ================================================================
# a = Argparse()

# def set_txt(ev=None):
#     doc["output"].value = a.__str__()

# doc["output"].bind("click", set_txt)

# debug
from browser import alert

a = Argument()
alert(a.inputs)
alert(str(a))
# a.remove()
# a = Argument()