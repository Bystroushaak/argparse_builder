# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import document as doc
from browser import html

# Variables ===================================================================
_ARG_COUNTER = range(100000).__iter__()  # argument table ID pool


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
    doc[ID + "_argument_type"].bind("change", select_to_string)

    arg = arg_from_id(ID)
    add_removable_help(
        arg.get(selector="input") + arg.get(selector="textarea")
    )


def select_to_string(ev):
    if ev.target.value == "custom":
        ID = ev.target.id
        ev.target.outerHTML = "<input type='text' name='type' id='%s' />" % ID


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
    """
    Get matching `argument` from subelement `target`.

    Args:
        target (HTML element): Button, input or any subelement in argument with
                               proper ``.id``.

    Returns:
        HTML element: `argument` table containing given `target`.
    """
    return arg_from_id(id_from_target(target))


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



def get_id_from_pool():
    """
    Returns:
        int: Incremented ID from previous call.
    """
    return _ARG_COUNTER.__next__()


# Animations ==================================================================
def add_argument(ev=None):
    ID = str(get_id_from_pool())

    template = doc["argument_template"].innerHTML

    table = html.TABLE(id=ID+"_argument", Class="argument_table")
    table.html = template.replace("$ID", ID)
    doc["arguments"] <= table

    add_callbacks(ID)


def remove_argument(ev):
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
add_removable_help(doc.get(selector="input") + doc.get(selector="textarea"))


# debug =======================================================================
# doc["output"].value = str(get_list_of_arguments())
# doc["output"].value += str()