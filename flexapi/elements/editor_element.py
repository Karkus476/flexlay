# Flexlay - A Generic 2D Game Editor
# Copyright (C) 2016 Karkus476 <karkus476@yahoo.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import QWidget, QVBoxLayout, QTabWidget

from .flexlay_element import FlexlayElement
from ..flexlay_error import FlexlayError
from ..tabs.editor_tab import EditorTab
from ..resources.path_resource import PathResource


class EditorElement(FlexlayElement):
    """This element is used to edit files

    Either simple text files, with or without syntax highlighting, or tile maps, or scripts or anything!
    """
    def __init__(self):
        super().__init__()
        # List of classes which can be instantiated as tabs
        self.tab_types = []
        # Currently open tabs.
        self._tabs = {}
        # The QTabWidget in which all the tabs appear. The internal PyQt part of the element
        self.tab_widget = None

    def add_tab_type(self, Tab):
        # Validation? Tab is subclass?
        self.tab_types.append(Tab)

    def edit(self, tab_label, item):
        """Open a new tab to edit or view item

        Parameters:
            tab_label - the visible label at the top of the tab
            item - the resource (most likely) or value to be edited.
        """
        # Sorts the classes by can_edit return value in self.tab_types into a list of tuples (Tab, can_edit value)
        sorted_preference = sorted([(TabType, TabType.can_edit(item)) for TabType in self.tab_types], key=lambda x:x[1])
        # Ensure a working tab is found which has a value not 0
        if len(sorted_preference) > 0 and sorted_preference[-1][1] > 0:
            Tab = sorted_preference[-1][0]
        else:
            raise FlexlayError("No tabs capable of editing item: " + str(item) + " of type " + type(item))
        # Create a new tab of this type.
        self.add_tab(tab_label, Tab(item))

    def write(self, index):
        """Write the specified tab's current status, presumably to a file. Doesn't apply to all tabs."""
        self._tabs[index].write()

    def write_current(self, path_resource):
        """Run write method on the currently selected tab"""
        pass

    def add_tab(self, label, tab):
        """Add a new tab to the element

        Parameters:
            label - The label to appear at the top of the tab
            tab - The EditorTab which will be visible.
        """
        if not isinstance(tab, EditorTab):
            raise FlexlayError("'tab' added which is not EditorTab!")
        self.tab_widget.addTab(tab.get_widget(), label)

    def added_to(self, editor):
        super().added_to(editor)
        self.tab_widget = QTabWidget(editor.window)
        editor.window.setCentralWidget(self.tab_widget)

    def removed(self):
        super().removed()
        self.tab_widget = None