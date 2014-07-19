# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from browser import html
from browser import document as doc

from collections import OrderedDict


# Variables ===================================================================
_ARG_COUNTER = range(100000).__iter__()  # argument table ID pool

ARG_PARSER_TEMPLATE = """import argparse

# ...
parser = argparse.ArgumentParser($parameters)
$arguments
args = parser.parse_args()

"""

ARG_TEMPLATE = """parser.add_argument(
\t$parameters
)
"""


# Functions & objects =========================================================
def hide_help_frame(ev):
    """
    Remove help popup from the HTML.
    """
    doc["help_placeholder"].innerHTML = ""
    doc["black_overlay"].style.display = "none"


def show_help_frame(ev):
    """
    Add help popup to the HTML.
    """
    src = '<iframe id="white_content" src="' + ev.target.fhref + '"></iframe>'

    doc["help_placeholder"].innerHTML = src
    doc["black_overlay"].style.display = "inline"
    doc["white_content"].style.display = "inline"


def bind_links(container):
    """
    Bind all links in given `container` to popup help/iframe.

    Note:
        This function can be called only once for each link, or it wouln't work.
    """
    # bind all links to show popup with help
    for el in container.get(selector="a"):
        el.fhref = el.href
        el.href = "#"
        el.bind("click", show_help_frame)


def parse_arguments(ev):
    """
    Parse arguments from inputs and save the result to the output textarea.
    """
    text = a.__str__()

    if doc["output_use_spaces"].checked:
        text = text.replace("\t", "    ")

    doc["output"].value = text


def get_id_from_pool():
    """
    Returns:
        int: Incremented ID from previous call.
    """
    return _ARG_COUNTER.__next__()


def type_on_change_event(self, ev):
    """
    This code switches select for input when user selects `Custom` in
    `type` select element.
    """
    if ev.target.value == "custom":
        ID = self.element.id
        new_html = '<input id="%s" type="text" _non_str="true" ' % ID
        new_html += '_non_key="" _default="" />'
        ev.target.outerHTML = new_html

        self.element = doc[ID]


def action_on_change_event(self, ev):
    """
    Event raised when user changes value in `action` input.
    """
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

    # enable/disable other inputs
    disabled = (ev.target.value in bool_switches)
    disabled_inputs = map(lambda x: self.parent.inputs[x], bool_disables)

    for item in disabled_inputs:
        item.disabled = disabled


class ArgInput(object):
    """
    This class is used to wrap <input>, <select> and <textarea> HTML elements.

    It provides unified setters and getters for those elements, allows to
    define callbacks when clicked/changed, switch two :class:`ArgInput` objects,
    serialize them to string, enable/disable them and so on.

    Attr:
        ID (str): Unique ID. Thanks to this, objects know which HTML elements
                  belong to them.
        name (str): Name of the argparse argument - `descr`, `type` and so on.
        parent (str): Pointer to :class:`Argument`, where this object is stored.
                      This can be usedd to disable other inputs and so on.
        element (obj): Pointer to HTML element.
        is_text_type (bool): True for inputs/textareas, false for select,
                             checkboxes and others.
        wrapped_value (str): Value used when element is serialized to python.
        value (str): Clean value of the element.
        disabled (bool): Property which allows to enable/disable HTML element.
    """
    def __init__(self, element, parent):
        self.ID = element.id.split("_")[0]
        self.name = element.id.split("_")[-1]

        self.parent = parent
        self.element = element  # reference to html object

        if self.element.value == "":
            self.element.value = self.element.title

        if self.is_text_type:
            element.bind("focus", self.input_remove_help_callback)
            element.bind("blur", self.input_add_help_callback)
        elif element.nodeName == "SELECT":
            element.bind("change", self.on_change_callback)

        self.on_change_events = {
            "type": type_on_change_event,
            "action": action_on_change_event
        }

    def on_change_callback(self, ev):
        """
        Callback called every time the select HTML element is changed.
        """
        func = self.on_change_events.get(self.name, None)

        if func:
            func(self, ev)

    def input_remove_help_callback(self, ev):
        """
        Called when user clicks to the input/textarea element to remove help.
        """
        if ev.target.value == ev.target.title:
            ev.target.value = ""

    def input_add_help_callback(self, ev):
        """
        Called every time user removes focus from input element to restere
        help, if the input is blank.
        """
        if ev.target.value == "":
            ev.target.value = ev.target.title

    @property
    def wrapped_value(self):
        """
        Property to wrap the internal raw value to string.

        This is used for string serialization - some of the elements needs to
        add quotes, some have default values and so on.
        """
        if self.disabled:
            return None

        # selects
        if not self.is_text_type and \
           self.element.value == self.element._default:
            return None

        # checkboxes
        if self.element.type == "checkbox":
            value = self.element.checked

            if self.element._default == str(value):
                return None

            return value

        # text elements - textearea/input
        if self.element.value != self.element.title:
            if self.element._non_str.strip():
                return self.element.value

            val = self.element.value.replace(r"\\", r"\\")  # don't even ask

            quote = '"'
            if "\n" in val:
                quote = quote * 3

            if quote in val:
                val = val.replace(quote, quote.replace('"', '\\"'))

            return quote + val + quote

        return None

    @property
    def value(self):
        """
        Property to access value of the HTML element.
        """
        if self.element.type == "checkbox":
            return self.element.checked

        return self.element.value

    @value.setter
    def value(self, new_val):
        """
        Property to set value of the HTML element.
        """
        if self.element.type == "checkbox":
            self.element.checked = new_val
        else:
            self.element.value = new_val

    @property
    def is_text_type(self):
        """
        Getter showing whether the ArgInput object wraps text element or
        switch/checkbox.
        """
        return self.element.type == "text" or \
               self.element.nodeName == "TEXTAREA"

    @property
    def disabled(self):
        """
        Abstration over disabled property.
        """
        return self.element.disabled

    @disabled.setter
    def disabled(self, val):
        """
        Setteer for diabled property.
        """
        self.element.disabled = val

    def switch(self, inp2):
        """
        Switch two ArgInput objects.

        Switch values, if the objects are of the same type, or whole HTML
        elements, if they are different types.

        Args:
            inp2 (object): :class:`ArgInput` class.
        """
        inp1 = self

        if inp1.element.nodeName != inp2.element.nodeName:
            val1, val2 = inp1.value, inp2.value
            inp1.element.id, inp2.element.id = inp2.element.id, inp1.element.id
            inp1.element.outerHTML, inp2.element.outerHTML = (
                inp2.element.outerHTML,
                inp1.element.outerHTML
            )
            inp1.element = doc[inp1.ID + "_argument_" + inp1.name]
            inp2.element = doc[inp2.ID + "_argument_" + inp2.name]
            inp1.value, inp2.value = val2, val1
        else:
            inp1.value, inp2.value = inp2.value, inp1.value

    def __str__(self):
        if self.element._non_key:
            return str(self.wrapped_value)

        return self.name + "=" + str(self.wrapped_value)


class Argument(object):
    """
    This object is used to represent sets of :class:`ArgInput` objects, in order
    as they are defined in <span> with ID `arguments`.

    It can also :func:`remove` itself from the HTML page and serialize content
    of the inputs to python code.

    Attr:
        ID (str): Unique ID. Thanks to this, objects know which HTML elements
                  belong to them.
        element (obj): Pointer to corresponding HTML table with inputs.
        inputs (ordered dict): Dictionary with HTML inputs stored in format
               ``{"$NAME": el_reference}`` where ``$NAME`` is last part of
               HTML `id` splitted by ``_``.
    """
    def __init__(self):
        self.ID = str(get_id_from_pool())
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

        bind_links(self.element)

    def _add_html_repr(self):
        """
        Add HTML representation of the argument to the HTML page.
        """
        template = doc["argument_template"].innerHTML

        table = html.TABLE(id=self.ID + "_argument", Class="argument_table")
        table.html = template.replace("$ID", self.ID)
        doc["arguments"] <= table

        return table

    def remove(self):
        """
        Remove argument from HTML.
        """
        doc[self.ID + "_argument"].outerHTML = ""

    def switch(self, arg2):
        """
        Switch all values in this Argument with `arg2`.
        """
        assert isinstance(arg2, Argument)

        for key in self.inputs.keys():
            self.inputs[key].switch(arg2.inputs[key])

    def __str__(self):
        # collect strings from all inputs
        vals = map(
            lambda x: str(x),
            filter(
                lambda x: x.wrapped_value is not None,
                self.inputs.values()
            )
        )

        if len(list(vals)) == 0:
            return ""

        return ARG_TEMPLATE.replace(
            "$parameters",
            ",\n\t".join(vals)
        )


class ArgParser(object):
    """
    This object holds references to all argument tables and global argparse
    settings.

    Attr:
        arguments (ordered dict): References to :class:`Argument` objects.
        element (obj): Reference to `argument_parser` <span>.
        inputs (ordered dict): Reference to global settings inputs.
    """
    def __init__(self):
        self.arguments = OrderedDict()
        self.add_argument_callback()

        # parse all inputs belonging to the argparser objects
        self.element = doc["argument_parser"]
        arguments = self.element.get(selector="input")
        arguments += self.element.get(selector="textarea")
        self.inputs = OrderedDict(
            map(
                lambda x: (x.id.split("_")[-1], ArgInput(x, self)),
                sum(arguments, [])
            )
        )

    def new_argument(self):
        """
        Create new :class:`Argument` object and bind events to the buttons.

        Returns:
            Argument object: Created object.
        """
        arg = Argument()
        self.bind_argument(arg)
        return arg

    def bind_argument(self, argument):
        """
        Bind buttons in `argument` object to callbacks methods in this object.
        """
        doc[argument.ID + "_argument_button_add"].bind(
            "click",
            self.add_argument_callback
        )
        doc[argument.ID + "_argument_button_rm"].bind(
            "click",
            self.remove_argument_callback
        )
        doc[argument.ID + "_argument_button_up"].bind(
            "click",
            self.move_arg_up_callback
        )
        doc[argument.ID + "_argument_button_down"].bind(
            "click",
            self.move_arg_down_callback
        )

    def add_argument_callback(self, ev=None):
        """
        Add new argument into HTML representation and internal dict.

        Note:
            This method is called asynchronously, when the button is pressed.
        """
        arg = self.new_argument()
        self.arguments[arg.ID] = arg

    def remove_argument_callback(self, ev=None):
        """
        Remove argument from HTML representation and internal dict.

        ID of the argument is parsed from `ev` parameter.

        Note:
            This method is called asynchronously, when the button is pressed.
        """
        if len(self.arguments) > 1:
            ID = ev.target.id.split("_")[0]
            self.arguments[ID].remove()
            del self.arguments[ID]

    def move_arg_up_callback(self, ev):
        """
        Switch two arguments - move the argument where the button was pressed
        down.

        Note:
            This method is called asynchronously, when the button is pressed.
        """
        ID = ev.target.id.split("_")[0]
        keys = list(self.arguments.keys())
        ioa = keys.index(ID)

        if len(self.arguments) > 1 and ioa > 0:
            arg1 = self.arguments[keys[ioa]]
            arg2 = self.arguments[keys[ioa - 1]]

            arg1.switch(arg2)

    def move_arg_down_callback(self, ev=None):
        """
        Switch two arguments - move the argument where the button was pressed
        down.

        Note:
            This method is called asynchronously, when the button is pressed.
        """
        ID = ev.target.id.split("_")[0]
        keys = list(self.arguments.keys())
        ioa = keys.index(ID)

        if len(self.arguments) > 1 and ioa < len(self.arguments) - 1:
            arg1 = self.arguments[keys[ioa]]
            arg2 = self.arguments[keys[ioa + 1]]

            arg1.switch(arg2)

    def __str__(self):
        # read value of all inputs in this object
        vals = map(
            lambda x: str(x),
            # pick only inputs with value
            filter(
                lambda x: x.wrapped_value is not None,
                self.inputs.values()
            )
        )

        # add \n\t only if there are used inputs
        inp_string = "\n\t".join(vals)
        if inp_string:
            inp_string = ",\n\t" + inp_string + "\n"

        # put inputs to template
        out = ARG_PARSER_TEMPLATE.replace("$parameters", inp_string)

        # convert arguments to strings
        arguments = ""
        for item in self.arguments.values():
            arguments += item.__str__()

        # put arguments to template
        return out.replace("$arguments", arguments)


# Main program ================================================================
a = ArgParser()

# bind click on output textarea with generation of the source code
doc["output"].bind("click", parse_arguments)
doc["output_use_spaces"].bind("click", parse_arguments)

# bind links with popup help
doc["black_overlay"].bind("click", hide_help_frame)
bind_links(doc["argument_parser"])
