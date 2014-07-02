#! /usr/bin/env python
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


def input_from_type_id(ID, el_type):
    return doc[ID + "_argument_" + el_type]


def get_id_from_pool():
    """
    Returns:
        int: Incremented ID from previous call.
    """
    return _ARG_COUNTER.__next__()
