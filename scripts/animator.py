# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
from browser import html

import argtools


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
    doc[ID + "_argument_type"].bind("change", select_to_text)
    doc[ID + "_argument_action"].bind("change", disable_other_inputs)

    arg = argtools.arg_from_id(ID)
    add_removable_help(
        arg.get(selector="input") + arg.get(selector="textarea")
    )


def add_removable_help(clickable):
    """
    Adds and removes help on focus.

    Args:
        clickable (list): List of HTML elements.
    """
    def input_remove_help(ev):
        if ev.target.value == ev.target.title:
            ev.target.value = ""

    def input_add_help(ev):
        if ev.target.value == "":
            ev.target.value = ev.target.title

    for item in clickable:
        item.bind("focus", input_remove_help)
        item.bind("blur", input_add_help)

        # add help to the .value
        if item.type == "text" or item.nodeName == "TEXTAREA":
            item.value = item.title


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


def index_of_argument(arg, args=None):
    """
    Returns index of given argument in array of arguments visible at page.

    Args:
        arg (str): Argument for which index you are looking for.
        args (list, default None): Optional list which will be used to look for
                                   `arg`. If not set, get_list_of_arguments() is
                                   used.

    Returns:
        int: Index of argument in array or ValueError if not found.

    Raises:
        ValueError: If `arg` is not found.
    """
    if not args:
        args = get_list_of_arguments()

    return args.index(arg)


def switch_values(arg1, arg2):
    """
    Switch .value properties in corresponding input/textarea child from both
    elements.

    Args:
        arg1 (HTML element): First element.
        arg2 (HTML element): Second element.
    """
    # I've tried to rewrite this to map, but writing elements selectors
    # explicitly makes it MUCH more faster (like 0.1s vs 2s)
    items = zip(
        sorted(
            arg1.get(selector="textarea") +
            arg1.get(selector="input") +
            arg1.get(selector="select"),
            key=lambda x: x.id
        ),
        sorted(
            arg2.get(selector="textarea") +
            arg2.get(selector="input") +
            arg2.get(selector="select"),
            key=lambda x: x.id
        )
    )

    for item1, item2 in items:
        # switch whole elements for different kinds of inputs (select vs text)
        if item1.nodeName != item2.nodeName:
            # save values
            v1, v2 = item1.value, item2.value

            # switch ID
            item1.id, item2.id = item2.id, item1.id

            # switch elements
            item1.outerHTML, item2.outerHTML = item2.outerHTML, item1.outerHTML

            # restore saved values
            doc[item1.id].value, doc[item2.id].value = v1, v2
            continue

        # elements of same type switches just titles and values
        item1.value, item2.value = item2.value, item1.value
        item1.title, item2.title = item2.title, item1.title


# Animations ==================================================================
def add_argument(ev=None):
    """
    Add new argument table.
    """
    ID = str(argtools.get_id_from_pool())

    template = doc["argument_template"].innerHTML

    table = html.TABLE(id=ID+"_argument", Class="argument_table")
    table.html = template.replace("$ID", ID)
    doc["arguments"] <= table

    add_callbacks(ID)


def remove_argument(ev):
    """
    Remove argument table.
    """
    if len(get_list_of_arguments()) > 1:
        argtools.arg_from_target(ev.target).outerHTML = ""


def move_argument_up(ev):
    """
    Switch two arguments.
    """
    arg = argtools.arg_from_target(ev.target)
    arguments = get_list_of_arguments()

    if len(arguments) > 1:
        ioa = index_of_argument(arg, arguments)
        if ioa > 0:
            switch_values(arguments[ioa - 1], arg)


def move_argument_down(ev):
    """
    Switch two arguments.
    """
    arg = argtools.arg_from_target(ev.target)
    arguments = get_list_of_arguments()

    if len(arguments) > 1:
        ioa = index_of_argument(arg, arguments)
        if ioa < len(arguments) - 1:
            switch_values(arg, arguments[ioa + 1])


def select_to_text(ev):
    """
    Convert select with "custom" value to text input.
    """
    if ev.target.value == "custom":
        ID = ev.target.id
        ev.target.outerHTML = "<input type='text' name='type' id='%s' />" % ID


def disable_other_inputs(ev):
    def set_diabled(ID, items, state):
        for item in items:
            argtools.input_from_type_id(ID, item).disabled = state

    ID = argtools.id_from_target(ev.target)
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

    if ev.target.value in bool_switches:
        set_diabled(ID, bool_disables, True)
    else:
        set_diabled(ID, bool_disables, False)


# Main script =================================================================
add_argument()
add_removable_help(doc.get(selector="input") + doc.get(selector="textarea"))
