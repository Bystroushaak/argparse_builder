# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================
def add_argument_element(ev):
    template = doc["argument_template"]
    doc["arguments"].innerHTML = doc["arguments"].innerHTML + template.outerHTML


# Functions & objects =========================================================



# Main program ================================================================
doc['argument_button'].bind('click', add_argument_element)