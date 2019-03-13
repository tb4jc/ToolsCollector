#
# Package that contains helper functions missing in PySide to support similar functionality
# as provided by PyQt.
#

import xml.etree.ElementTree as xml
from io import StringIO
import pyside2uic
from PySide2 import QtWidgets


def loadUiType(filename):
    """Load form class from ui file."""
    parsed = xml.parse(filename)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(filename, 'r') as f:
        o = StringIO()
        frame = {}
        pyside2uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        ret_val = exec(pyc, frame)
        # exec(pyc) in frame
        form_class = frame['Ui_%s'%form_class]
        base_class = eval('QtWidgets.%s'%widget_class)
    return form_class, base_class


def loadUi(filename, obj):
    """
    Load ui form class onto a given QWidget object.

    NOTE:
    This implements only the most common usage of PyQt's uic.loadUi as
    done in `__init__` with `uic.loadUi('/some/ui/file', self)` meaning
    the initializing class gets decorated with the form class from the
    ui file itself.
    Feel free to implement missing API features like a return value.
    """
    form_cls, base_cls = loadUiType(filename)
    cls = obj.__class__
    obj.__class__ = cls.__class__(
        cls.__name__ + form_cls.__name__, (cls, form_cls), {})
    obj.setupUi(obj)
