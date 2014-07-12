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
def type_on_change_event(self, ev):
    if ev.target.value == "custom":
        ID = self.element.id
        new_html = '<input id="%s" type="text" _non_str="true" ' % ID
        new_html += '_non_key="" _default="" />'
        ev.target.outerHTML = new_html

        self.element = doc[ID]


def action_on_change_event(self, ev):
    bool_switches = [
        "count",
        "store_true",
        "store_false",
        "help",
        "version"
    ]
    bool_disables = [
        "type",
        "const",
        "nargs",
        "choices",
        "default",
        "metavar"
    ]

    disabled = (ev.target.value in bool_switches)
    disabled_inputs = map(lambda x: self.parent.inputs[x], bool_disables)

    for item in disabled_inputs:
        item.disabled = disabled


class ArgInput(object):
    def __init__(self, element, parent):
        self.parent = parent
        self.ID = element.id.split("_")[0]
        self.name = element.id.split("_")[-1]
        self.element = element

        if self.element.value == "":
            self.element.value = self.element.title

        if self.is_text_type:
            element.bind("focus", self.input_remove_help)
            element.bind("blur", self.input_add_help)
        elif element.nodeName == "SELECT":
            element.bind("change", self.on_change)

        self.on_change_events = {
            "type": type_on_change_event,
            "action": action_on_change_event
        }

    def on_change(self, ev):
        func = self.on_change_events.get(self.name)

        if func:
            func(self, ev)

    def input_remove_help(self, ev):
        if ev.target.value == ev.target.title:
            ev.target.value = ""

    def input_add_help(self, ev):
        if ev.target.value == "":
            ev.target.value = ev.target.title

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

    def get_raw_value(self):
        if self.element.type == "checkbox":
            return self.element.checked

        return self.element.value

    @value.setter
    def value(self, new_val):
        if self.element.type == "checkbox":
            self.element.checked = new_val
        else:
            self.element.value = new_val

    @property
    def is_text_type(self):
        return self.element.type == "text" or self.element.nodeName == "TEXTAREA"

    @property
    def disabled(self):
        return self.element.disabled

    @disabled.setter
    def disabled(self, val):
        self.element.disabled = val

    def switch(self, inp2):
        inp1 = self

        if inp1.element.nodeName != inp2.element.nodeName:
            val1, val2 = inp1.get_raw_value(), inp2.get_raw_value()
            inp1.element.id, inp2.element.id = inp2.element.id, inp1.element.id
            inp1.element.outerHTML, inp2.element.outerHTML = (
                inp2.element.outerHTML,
                inp1.element.outerHTML
            )
            inp1.element = doc[inp1.ID + "_argument_" + inp1.name]
            inp2.element = doc[inp2.ID + "_argument_" + inp2.name]
            inp1.value, inp2.value = val2, val1
        else:
            inp1.value, inp2.value = inp2.get_raw_value(), inp1.get_raw_value()

    def __str__(self):
        if self.element._non_key:
            return str(self.value)

        return self.name + "=" + str(self.value)


class Argument(object):
    def __init__(self):
        self.ID = str(argtools.get_id_from_pool())
        self.element = self._add_html_repr()

        arguments = self.element.get(selector="input")
        arguments = list(filter(lambda x: x.type != "button", arguments))
        arguments += self.element.get(selector="select")
        arguments += self.element.get(selector="textarea")
        self.inputs = OrderedDict(
            map(
                lambda x: (x.id.split("_")[-1], ArgInput(x, self)),
                sum(arguments, [])
            )
        )

    def _add_html_repr(self):
        """
        Add new argument table.
        """
        template = doc["argument_template"].innerHTML

        table = html.TABLE(id=self.ID + "_argument", Class="argument_table")
        table.html = template.replace("$ID", self.ID)
        doc["arguments"] <= table

        return table

    def remove(self):
        doc[self.ID + "_argument"].outerHTML = ""

    def switch(self, arg2):
        assert isinstance(arg2, Argument)

        for key in self.inputs.keys():
            self.inputs[key].switch(arg2.inputs[key])

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


class ArgParser(object):
    def __init__(self):
        self.arguments = OrderedDict()
        self.add_argument()

    def bind_argument(self, argument):
        doc[argument.ID + "_argument_button_add"].bind(
            "click",
            self.add_argument
        )
        doc[argument.ID + "_argument_button_rm"].bind(
            "click",
            self.remove_argument
        )
        doc[argument.ID + "_argument_button_up"].bind(
            "click",
            self.move_arg_up
        )
        doc[argument.ID + "_argument_button_down"].bind(
            "click",
            self.move_arg_down
        )

    def move_arg_up(self, ev):
        ID = ev.target.id.split("_")[0]
        keys = list(self.arguments.keys())
        ioa = keys.index(ID)

        if len(self.arguments) > 1 and ioa > 0:
            arg1 = self.arguments[keys[ioa]]
            arg2 = self.arguments[keys[ioa - 1]]

            arg1.switch(arg2)

    def move_arg_down(self, ev=None):
        ID = ev.target.id.split("_")[0]
        keys = list(self.arguments.keys())
        ioa = keys.index(ID)

        if len(self.arguments) > 1 and ioa < len(self.arguments) - 1:
            arg1 = self.arguments[keys[ioa]]
            arg2 = self.arguments[keys[ioa + 1]]

            arg1.switch(arg2)

    def new_argument(self):
        arg = Argument()
        self.bind_argument(arg)
        return arg

    def add_argument(self, ev=None):
        arg = self.new_argument()
        self.arguments[arg.ID] = arg

    def remove_argument(self, ev=None):
        if len(self.arguments) > 1:
            ID = ev.target.id.split("_")[0]
            self.arguments[ID].remove()
            del self.arguments[ID]

    def __str__(self):
        out = ""
        for item in self.arguments.values():
            out += item.__str__()

        out = ARG_PARSER_TEMPLATE.replace("$arguments", out)

        return out


# Main program ================================================================
a = ArgParser()

def set_txt(ev=None):
    doc["output"].value = a.__str__()

doc["output"].bind("click", set_txt)

# debug
from browser import alert

# a = Argument()
# alert(a.inputs)
# alert(str(a))
# a.remove()
# a = Argument()