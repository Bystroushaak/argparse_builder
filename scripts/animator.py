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
ARG_COUNTER = 0  # Increment only counter used as pool for ID / new arguments


# Functions & objects =========================================================
def add_callbacks(ID):
    """
    Adds all callbacks for argument table with given `ID`.

    Args:
        ID (number): ID of selected argument table.
    """
    ID = str(ID)
    doc[ID + "_argument_button_add"].bind("click", add_argument)
    doc[ID + "_argument_button_rm"].bind("click", remove_argument)
    doc[ID + "_argument_button_up"].bind("click", move_argument_up)
    doc[ID + "_argument_button_down"].bind("click", move_argument_down)


def get_list_of_arguments():
    """
    Returns:
        list: of HTML objects with argument tables (argument_table class).
    """
    docs = doc.get(selector="table.argument_table")
    return list(
        filter(
            lambda x: x.id != "argument_template",  # skip template
            docs
        )
    )


def defaults_to_values():
    """
    Goes thru all inputs/textareas and puts content their .title property to
    .value, if value is not already set.
    """
    for key in doc[html.INPUT] + doc[html.TEXTAREA]:
        if key.value.strip():  # skip already filled values
            continue

        if key.type == "text" or key.nodeName == "TEXTAREA":
            key.value = key.title


def id_from_target(target):
    """
    Return `ID` number from given target.

    Args:
        target (HTML element): DOM node with .id property in format id_rest.

    Returns:
        str: ID number in string (I don't really need int).
    """
    return target.id.split("_")[0]


def arg_from_id(ID):
    """
    Return argument matching given ID.

    Args:
        ID (str): ID used to search in DOM

    Returns:
        HTML element: Matching element.
    """
    return doc[ID + "_argument"]


def arg_from_target(target):
    return arg_from_id(id_from_target(target))


def index_of_argument(arg, args=None):
    if not args:
        args = get_list_of_arguments()

    return args.index(arg)


def switch_values(arg1, arg2):
    items = zip(
        arg1.get(selector="input") + arg1.get(selector="textarea"),
        arg2.get(selector="input") + arg2.get(selector="textarea")
    )

    for item1, item2 in items:
        item1.value, item2.value = item2.value, item1.value


# Animations ==================================================================
def add_argument(ev=None):
    global ARG_COUNTER

    ARG_COUNTER += 1
    ID = str(ARG_COUNTER)  # get new ID from pool

    template = doc["argument_template"].innerHTML

    table = html.TABLE(id=ID+"_argument", Class="argument_table")
    table.html = template.replace("$ID", ID)
    doc["arguments"] <= table

    add_callbacks(ID)
    defaults_to_values()


def remove_argument(ev):
    global ARG_COUNTER

    if len(get_list_of_arguments()) > 1:
        arg_from_target(ev.target).outerHTML = ""

def move_argument_up(ev):
    arg = arg_from_target(ev.target)
    arguments = get_list_of_arguments()

    if len(arguments) > 1:
        ioa = index_of_argument(arg, arguments)
        if ioa > 0:
            switch_values(arguments[ioa - 1], arg)


def move_argument_down(ev):
    arg = arg_from_target(ev.target)
    arguments = get_list_of_arguments()

    if len(arguments) > 1:
        ioa = index_of_argument(arg, arguments)
        if ioa < len(arguments) - 1:
            switch_values(arg, arguments[ioa + 1])


# Main program ================================================================
add_argument()

# debug =======================================================================
# doc["output"].value = str(get_list_of_arguments())
# doc["output"].value += str()