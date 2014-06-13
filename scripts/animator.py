# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
from browser import html

# Variables ===================================================================
ARG_PARAMS = [
    "flag",
    "name",
    "action",
    "nargs",
    "const",
    "default",
    "type",
    "choices",
    "required",
    "metavar",
    "dest",
    "help"
]
ARG_COUNTER = 0  # used as ID of new arguments


# Functions & objects =========================================================
def add_callbacks(ID):
    doc[ID + "_argument_button_add"].bind("click", add_argument_element)


def add_argument_element(ev=None):
    global ARG_COUNTER
    ARG_COUNTER += 1
    ID = str(ARG_COUNTER)

    table = html.TABLE(id=ID+"argument", Class="argument_table")
    template = doc["argument_template"].innerHTML
    table.html = template.replace("$ID", ID)
    doc["arguments"] <= table
    
    add_callbacks(ID)
    defaults_to_values()


# Main program ================================================================
add_argument_element()